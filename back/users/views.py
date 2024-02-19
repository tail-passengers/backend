from rest_framework import viewsets
from .serializers import UsersSerializer, FriendRequestSerializer
from .models import Users, FriendRequests


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequests.objects.all()
    serializer_class = FriendRequestSerializer
