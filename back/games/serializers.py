from rest_framework import serializers
from .models import (
    GeneralGameLogs,
    TournamentGameLogs,
    JoinGeneralGame,
    JoinTournamentGame,
)
from accounts.serializers import UsersSerializer


class GeneralGameLogsSerializer(serializers.ModelSerializer):
    user_request = UsersSerializer(many=True, read_only=True)

    class Meta:
        model = GeneralGameLogs
        fields = (
            "game_id",
            "start_time",
            "end_time",
            "winner",
            "loser",
            "user_request",
        )


class JoinGeneralGameSerializer(serializers.ModelSerializer):
    user_request = UsersSerializer(read_only=True)
    game_request = GeneralGameLogsSerializer(read_only=True)

    class Meta:
        model = JoinGeneralGame
        fields = (
            "game_id",
            "user_id",
            "user_request",
            "game_request",
        )


class TournamentGameLogsSerializer(serializers.ModelSerializer):
    user_request = UsersSerializer(many=True, read_only=True)

    class Meta:
        model = TournamentGameLogs
        fields = (
            "tournament_name",
            "round",
            "winner",
            "loser",
            "start_time",
            "end_time",
            "is_final",
            "user_request",
        )


class JoinTournamentGameSerializer(serializers.ModelSerializer):
    user_request = UsersSerializer(read_only=True)
    game_request = TournamentGameLogsSerializer(read_only=True)

    class Meta:
        model = JoinTournamentGame
        fields = (
            "game_id",
            "user_id",
            "user_request",
            "game_request",
        )
