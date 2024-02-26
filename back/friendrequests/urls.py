from django.urls import path
from . import views

urlpatterns = [
    path(
        "friend_requests/<uuid:user_id>/",
        views.FriendListViewSet.as_view({"get": "list"}),
    ),
    path(
        "friend_requests/<uuid:user_id>/<uuid:request_id>/",
        views.FriendRequestDetailViewSet.as_view(
            {
                "get": "list",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "friend_requests/<uuid:user_id>/<str:status>/",
        views.FriendListViewSet.as_view({"get": "list"}),
    ),
    path(
        "friend_requests/",
        views.FriendRequestViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    # path("", views.FriendRequestViewSet.as_view({"get": "list"})),
]
