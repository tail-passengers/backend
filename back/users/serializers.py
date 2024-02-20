from rest_framework import serializers
from .models import Users, FriendRequests


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


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
