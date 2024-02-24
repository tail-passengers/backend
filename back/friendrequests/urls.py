from django.urls import include, path
from rest_framework import routers
from . import views

# DefaultRouter
router = routers.DefaultRouter()
router.register("friend_requests", views.FriendRequestViewSet)

urlpatterns = [
    path(
        "friend_requests/<uuid:user_id>",
        views.FriendListViewSet.as_view({"get": "list"}),
    ),
    path(
        "friend_requests/",
        views.FriendRequestViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path("", include(router.urls)),
]
