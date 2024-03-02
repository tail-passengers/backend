from django.urls import path
from . import views


urlpatterns = [
    path(
        "general_game_logs/",
        views.GeneralGameLogsViewSet.as_view({"get": "list", "post": "create"}),
        name="general_game_logs",
    ),
    path(
        "general_game_logs/<str:intra_id>/",
        views.GeneralGameLogsListViewSet.as_view({"get": "list"}),
        name="general_game_logs_detail",
    ),
    path(
        "tournament_game_logs/",
        views.TournamentGameLogsViewSet.as_view({"get": "list", "post": "create"}),
        name="create_tournament_game_logs",
    ),
    path(
        "tournament_game_logs/users/<str:intra_id>/",
        views.TournamentGameLogsListViewSet.as_view({"get": "list"}),
        name="tournament_game_user_logs",
    ),
    path(
        "tournament_game_logs/tournament/<str:name>/",
        views.TournamentGameLogsListViewSet.as_view({"get": "list"}),
        name="tournament_name_logs",
    ),
]
