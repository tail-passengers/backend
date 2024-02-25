from django.utils import timezone
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

    # winner랑 loser가 동일하면 에러 발생
    # 데이터 유효성 검사는 1. model 수준에서 2. serializer에서 가능한데
    # 1. clean을 오버라이딩해서 Django의 폼 시스템이나 관리자 사이트에서 주로 유용
    # 2. api에서 유용
    def validate(self, data):
        if data["winner"] == data["loser"]:
            raise serializers.ValidationError("Winner and loser must be different.")
        # 시작 시간이 끝나는 시간보다 이전인지 확인
        if data["start_time"] >= data["end_time"]:
            raise serializers.ValidationError("End time must be later than start time.")
        # 끝나는 시간이 현재 시각보다 이후인지 확인
        if data["end_time"] > timezone.now():
            raise serializers.ValidationError("End time must not be in the future.")
        return data


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
