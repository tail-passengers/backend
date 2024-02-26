from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import FriendRequests
from .serializers import (
    FriendListSerializer,
    FriendRequestSerializer,
    FriendRequestDetailSerializer,
)


class FriendListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequests.objects.all()
    serializer_class = FriendListSerializer
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        queryset = self.queryset.filter(
            Q(request_user_id=user_id) | Q(response_user_id=user_id)
        )

        if "status" in kwargs:
            status = kwargs["status"]
            if status == "pending":
                queryset = self.queryset.filter(
                    Q(Q(request_user_id=user_id) | Q(response_user_id=user_id))
                    & Q(status="0")
                )
            elif status == "accepted":
                queryset = self.queryset.filter(
                    Q(Q(request_user_id=user_id) | Q(response_user_id=user_id))
                    & Q(status="1")
                )
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FriendRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequests.objects.all()
    serializer_class = FriendRequestSerializer
    http_method_names = [
        "post",
        "patch",
        "delete",
        "get",
    ]  # TODO debug를 위해 get 임시 추가
    lookup_field = "request_id"

    def create(self, request, *args, **kwargs):
        request_user_id = request.data.get("request_user_id")
        response_user_id = request.data.get("response_user_id")
        # TODO 친구 요청하는 것이 자기 자신인지 확인하는 로직 추가
        if request_user_id == response_user_id:
            raise ValidationError(
                {"detail": "친구 요청을 받는 사람은 자신이 될 수 없습니다."}
            )
        queryset = self.queryset.filter(
            Q(Q(request_user_id=request_user_id) & Q(response_user_id=response_user_id))
            | Q(
                Q(request_user_id=response_user_id)
                & Q(response_user_id=request_user_id)
            )
        )
        if queryset.exists():
            raise ValidationError({"detail": "이미 친구 요청을 보냈습니다."})
        return super().create(request, *args, **kwargs)


class FriendRequestDetailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = FriendRequests.objects.all()
    serializer_class = FriendRequestDetailSerializer
    http_method_names = ["get", "patch", "delete"]
    lookup_field = "request_id"

    def partial_update(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        instance = self.get_object()
        response_user_id = instance.response_user_id.user_id
        if response_user_id != user_id:
            raise ValidationError(
                {"detail": "자신이 아닌 다른 사람의 친구 요청을 거절할 수 없습니다."}
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs["user_id"]
        instance = self.get_object()
        response_user_id = instance.response_user_id.user_id
        request_user_id = instance.request_user_id.user_id
        if response_user_id != user_id and request_user_id != user_id:
            raise ValidationError(
                {"detail": "자신이 아닌 다른 사람의 친구 요청을 삭제할 수 없습니다."}
            )
        return super().destroy(request, *args, **kwargs)
