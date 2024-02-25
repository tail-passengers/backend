from django.urls import include, path
from rest_framework import routers
from . import views


# DefaultRouter
router = routers.DefaultRouter()
router.register("general_game_logs", views.GeneralGameLogsViewSet)
router.register("tournament_game_logs", views.TournamentGameLogsViewSet)
# API 지원 안 함
# router.register("join_general_game", views.JoinGeneralGameViewSet)
# router.register("join_tournament_game", views.JoinTournamentGameViewSet)

urlpatterns = [
    path(
        "general_game_logs/",
        views.GeneralGameLogsViewSet.as_view({"get": "list", "post": "create"}),
        name="general_game_logs",
    ),
    path(
        "general_game_logs/<uuid:fk>/",
        views.GeneralGameLogsViewSet.as_view({"get": "list"}),
    ),
    path(
        "tournament_game_logs/<uuid:fk>/",
        views.TournamentGameLogsViewSet.as_view({"get": "list"}),
    ),
    path(
        "tournament_game_logs/<str:name>/",
        views.TournamentGameLogsViewSet.as_view({"get": "list"}),
    ),
    path("", include(router.urls)),
]
