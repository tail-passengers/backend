from django.urls import include, path
from rest_framework import routers
from . import views
from django.conf import settings
from django.conf.urls.static import static


# DefaultRouter
router = routers.DefaultRouter()
router.register("Users", views.UsersViewSet)

urlpatterns = [path('', include(router.urls))] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
