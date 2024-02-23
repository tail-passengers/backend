from rest_framework import serializers

from back.accounts.serializers import UsersSerializer
from .models import Users, FriendRequests


class FriendRequestSerializer(serializers.ModelSerializer):
    friend_request = UsersSerializer(read_only=True)

    class Meta:
        model = FriendRequests
        fields = (
            "request_id",
            "request_user_id",
            "response_user_id",
            "status",
            "created_time",
            "updated_time",
            "friend_request",
        )
