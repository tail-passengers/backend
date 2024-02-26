from django.urls import include, path
from rest_framework import routers
from . import views
from .views import logout_view

# DefaultRouter
# router = routers.DefaultRouter()
# router.register("users", views.UsersViewSet)

urlpatterns = [
    path(
        "users/",
        views.UsersViewSet.as_view({"get": "list", "post": "create"}),
        name="users",
    ),
    path(
        "users/<uuid:pk>/",
        views.UsersDetailViewSet.as_view(
            {"get": "list", "patch": "partial_update", "delete": "destroy"}
        ),
        name="usersDetail",
    ),
    path("login/", views.Login42APIView.as_view()),
    path("login/42/callback/", views.CallbackAPIView.as_view()),
    path("logout/", logout_view, name="logout"),
]
