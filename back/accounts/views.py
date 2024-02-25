import os
import requests
import uuid
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from django.conf import settings
from dotenv import load_dotenv
from .serializers import UsersSerializer, UsersDetailSerializer
from .models import Users
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import logout



# https://squirmm.tistory.com/entry/Django-DRF-Method-Override-%EB%B0%A9%EB%B2%95
class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ["get", "post"]  # TODO debug를 위해 post 임시 추가

    def create(self, request, *args, **kwargs):
        """
        디버그용 post
        """
        intra_id = request.data.get("intra_id")
        if not intra_id:
            return Response(
                {"error": "intra_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # intra_id 중복 검사
        if Users.objects.filter(intra_id=intra_id).exists():
            return Response(
                {"error": "User with this intra_id already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 새로운 사용자 생성
        user = Users.objects.create_user(intra_id=intra_id)
        serializer = self.get_serializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Users.objects.all()
    serializer_class = UsersDetailSerializer
    http_method_names = ["get", "patch", "delete"]  # TODO delete 나중에 제거 예정

    # 우선 nickname과 profile_image를 제외한 모든 필드를 수정 불가로 설정
    can_not_change_fields = (
        "user_id",
        "password",
        "last_login",
        "is_superuser",
        "intra_id",
        "win_count",
        "lose_count",
        "created_time",
        "updated_time",
        "status",
        "is_staff",
        "is_active",
        "groups",
        "user_permissions",
    )

    def destroy(self, request, *args, **kwargs):
        """
        DELETE method override
        """
        instance = self.get_object()
        if request.user.pk != kwargs["pk"]:
            raise PermissionDenied(
                {"detail": "다른 사용자의 정보는 삭제할 수 없습니다."}
            )
        if instance.profile_image:
            try:
                os.remove(
                    os.path.join(settings.MEDIA_ROOT, instance.profile_image.name)
                )
            except FileNotFoundError:
                print("File not found")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH method override
        """
        if request.user.pk != kwargs["pk"]:
            raise PermissionDenied(
                {"detail": "다른 사용자의 정보는 수정할 수 없습니다."}
            )
        for field in self.can_not_change_fields:
            if request.data.get(field) is not None:
                raise PermissionDenied(
                    {"detail": f"{field}는 수정할 수 없는 필드입니다."}
                )
        instance = self.get_object()
        previous_image = instance.profile_image
        response = super().partial_update(request, *args, **kwargs)
        if previous_image and request.data.get("profile_image") is not None:
            os.remove(os.path.join(settings.MEDIA_ROOT, previous_image.name))
        return response


class Login42APIView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")

        load_dotenv()
        client_id = os.environ.get("CLIENT_ID")
        response_type = "code"
        redirect_uri = os.environ.get("REDIRECT_URI")
        state = str(uuid.uuid4())
        request.session["state"] = state
        oauth_42_api_url = "https://api.intra.42.fr/oauth/authorize"
        return redirect(
            f"{oauth_42_api_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}&state={state}"
        )


# https://soyoung-new-challenge.tistory.com/92
class CallbackAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")

        if (
            request.session.get("state")
            and not request.GET.get("state") == request.session["state"]
        ):
            raise ValidationError({"detail": "oauth중 state 검증 실패."})

        access_token = self._get_access_token(request)
        # 42 api에 정보 요청
        user_info_request = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = user_info_request.json()
        login_id = user_info["login"]
        image_address = user_info["image"]["versions"]["small"]
        user_instance, created = Users.objects.get_or_create(
            intra_id=login_id,
            nickname=login_id,
            status=0,
        )

        if created:
            response = requests.get(image_address)
            if response.status_code == 200:
                image_content = ContentFile(response.content)
                user_instance.profile_image.save(f"{login_id}.png", image_content)
            user_instance.save()
        # login
        login(request, user_instance)
        return redirect("http://127.0.0.1:8000/users/")

    def _get_access_token(self, request):
        load_dotenv()
        grant_type = "authorization_code"
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")
        code = request.GET.get("code")
        state = request.GET.get("state")
        redirect_uri = os.environ.get("REDIRECT_URI")
        data = {
            "grant_type": grant_type,
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "state": state,
            "redirect_uri": redirect_uri,
        }
        token_request = requests.post("https://api.intra.42.fr/oauth/token", data)
        token_response_json = token_request.json()
        return token_response_json.get("access_token")


def logout_view(request):
    logout(request)
    return redirect("/")
