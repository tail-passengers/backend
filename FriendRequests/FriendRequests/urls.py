from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static


# DefaultRouter
router = routers.DefaultRouter()
router.register("friend_requests", views.FriendRequestViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
