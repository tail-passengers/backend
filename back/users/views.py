import os
import requests
import uuid
from rest_framework import viewsets
from rest_framework.views import APIView
from django.shortcuts import redirect
from dotenv import load_dotenv
from .serializers import UsersSerializer
from .models import Users
from .serializers import UsersSerializer, FriendRequestSerializer
from .models import Users, FriendRequests


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequests.objects.all()
    serializer_class = FriendRequestSerializer


class Login42APIView(APIView):
    def get(self, request, *args, **kwargs):
        load_dotenv()
        client_id = os.environ.get("CLIENT_ID")
        response_type = "code"
        redirect_uri = "http://127.0.0.1:8000/user/42/callback"
        state = str(uuid.uuid4())

        oauth_42_api_url = "https://api.intra.42.fr/oauth/authorize"
        return redirect(
            f'{oauth_42_api_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type={response_type}&state={state}'
        )


class CallbackAPIView(APIView):
    def get(self, request, *args, **kwargs):
        access_token = self._get_access_token(request)
        #42 api에 정보 요청
        user_info_request = requests.get(
            "https://api.intra.42.fr/v2/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = user_info_request.json()
        login_id = user_info["login"]
        image_address = user_info["image"]["versions"]["small"]
        db_request_data = {"intra_id": login_id, "nickname": login_id, "win_count": 0,
                           "lose_count": 0, "status": 0}  # , "profile_image": image_address}

        # post 요청을 통해 db 업데이트 (프로필 이미지 업로드가 아직 불가)
        token_request = requests.post("http://127.0.0.1:8000/Users/", db_request_data)
        return redirect(
            "http://127.0.0.1:8000/Users/"
        )

    def _get_access_token(self, request):
        load_dotenv()
        grant_type = 'authorization_code'
        client_id = os.environ.get("CLIENT_ID")
        client_secret = os.environ.get("CLIENT_SECRET")
        code = request.GET.get('code')
        state = request.GET.get('state')
        redirect_uri = "http://127.0.0.1:8000/user/42/callback"
        data = {"grant_type": grant_type, "client_id": client_id, "client_secret": client_secret, "code": code,
                "state": state, "redirect_uri": redirect_uri}
        token_request = requests.post("https://api.intra.42.fr/oauth/token", data)
        token_response_json = token_request.json()
        return token_response_json.get("access_token")