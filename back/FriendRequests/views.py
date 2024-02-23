from rest_framework import viewsets, status


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequests.objects.all()
    serializer_class = FriendRequestSerializer
