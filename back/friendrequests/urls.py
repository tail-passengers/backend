from django.urls import path
from . import views

urlpatterns = [
    path(
        "friend_requests/<uuid:user_id>/<str:status>/",
        views.FriendListViewSet.as_view({"get": "list"}),
    ),
    path(
        "friend_requests/<uuid:request_id>/",
        views.FriendRequestDetailViewSet.as_view(
            {
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "friend_requests/",
        views.FriendRequestViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
]
