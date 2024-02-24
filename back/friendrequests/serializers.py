from rest_framework import serializers

from accounts.serializers import UsersSerializer
from .models import FriendRequests


class FriendListSerializer(serializers.ModelSerializer):
    friend_request = UsersSerializer(read_only=True)

    class Meta:
        model = FriendRequests
        fields = (
            "request_user_id",
            "response_user_id",
            "status",
            "friend_request",
        )


class FriendRequestSerializer(serializers.ModelSerializer):
    friend_request = UsersSerializer(read_only=True)

    class Meta:
        model = FriendRequests
        fields = (
            "request_user_id",
            "response_user_id",
            "friend_request",
        )
