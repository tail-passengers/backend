from django.urls import include, path
from rest_framework import routers
from . import views


# DefaultRouter
router = routers.DefaultRouter()
router.register("general_game_logs", views.GeneralGameLogsViewSet)
router.register("tournament_game_logs", views.TournamentGameLogsViewSet)
router.register("join_general_game", views.JoinGeneralGameViewSet)
router.register("join_tournament_game", views.JoinTournamentGameViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
