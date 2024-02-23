from django.urls import include, path
from rest_framework import routers
from . import views
from .views import logout_view

# DefaultRouter
router = routers.DefaultRouter()
router.register("users", views.UsersViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.Login42APIView.as_view()),
    path("login/42/callback/", views.CallbackAPIView.as_view()),
    path("logout/", logout_view, name="logout"),
]
