from django.urls import include, path
from rest_framework import routers
from . import views


# DefaultRouter
router = routers.DefaultRouter()
router.register("Users", views.UsersViewSet)

urlpatterns = [path('', include(router.urls))]
