from django.urls import include, path
from rest_framework import routers
from back.FriendRequests.migrations import views

# DefaultRouter
router = routers.DefaultRouter()
router.register("friend_requests", views.FriendRequestViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
