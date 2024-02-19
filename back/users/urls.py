from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static


# DefaultRouter
router = routers.DefaultRouter()
router.register("Users", views.UsersViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("42/", views.Login42APIView.as_view()),
    path("user/42/callback", views.CallbackAPIView.as_view()),
]
