from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import FriendRequests
from .serializers import FriendListSerializer, FriendRequestSerializer


class FriendListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequests.objects.all()
    serializer_class = FriendListSerializer
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        # 밑에 if문은 debug를 위한 임시 get
        if "user_id" not in kwargs:
            return super().list(request, *args, **kwargs)

        user_id = kwargs["user_id"]
        queryset = self.queryset.filter(
            Q(request_user_id=user_id) | Q(response_user_id=user_id)
        )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FriendRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequests.objects.all()
    serializer_class = FriendRequestSerializer
    http_method_names = ["post", "get"]  # TODO debug를 위해 get 임시 추가

    def create(self, request, *args, **kwargs):
        request_user_id = request.data.get("request_user_id")
        response_user_id = request.data.get("response_user_id")
        instance = self.get_object()
        if instance.user_id != request_user_id and instance.user_id != response_user_id:
            raise ValidationError(
                {"detail": "다른 사용자의 정보를 사용할 수 없습니다."}
            )
        elif request_user_id == response_user_id:
            return ValidationError({"detail": "자신에게 친구 요청을 보낼 수 없습니다."})

        queryset = self.queryset.filter(
            Q(Q(request_user_id=request_user_id) & Q(response_user_id=response_user_id))
            | Q(
                Q(request_user_id=response_user_id)
                & Q(response_user_id=request_user_id)
            )
        )
        if queryset.exists():
            return ValidationError({"detail": "이미 친구 요청을 보냈습니다."})
        return super().create(request, *args, **kwargs)
