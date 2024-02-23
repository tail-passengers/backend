from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .serializers import (
    GeneralGameLogsSerializer,
    TournamentGameLogsSerializer,
    JoinGeneralGameSerializer,
    JoinTournamentGameSerializer,
)
from .models import (
    GeneralGameLogs,
    TournamentGameLogs,
    JoinGeneralGame,
    JoinTournamentGame,
)


class GeneralGameLogsViewSet(viewsets.ModelViewSet):
    queryset = GeneralGameLogs.objects.all()
    serializer_class = GeneralGameLogsSerializer


class JoinGeneralGameViewSet(viewsets.ModelViewSet):
    queryset = JoinGeneralGame.objects.all()
    serializer_class = JoinGeneralGameSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:  # db의 무결성 제약 조건을 위반할 때 발생하는 에러
            raise ValidationError({"detail": "동일한 게임의 참가자가 이미 존재합니다."})


class TournamentGameLogsViewSet(viewsets.ModelViewSet):
    queryset = TournamentGameLogs.objects.all()
    serializer_class = TournamentGameLogsSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:  # db의 무결성 제약 조건을 위반할 때 발생하는 에러
            raise ValidationError({"detail": "동일한 게임이 이미 존재합니다."})


class JoinTournamentGameViewSet(viewsets.ModelViewSet):
    queryset = JoinTournamentGame.objects.all()
    serializer_class = JoinTournamentGameSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:  # db의 무결성 제약 조건을 위반할 때 발생하는 에러
            raise ValidationError({"detail": "동일한 게임의 참가자가 이미 존재합니다."})
