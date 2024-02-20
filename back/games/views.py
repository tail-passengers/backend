from rest_framework import viewsets
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


class TournamentGameLogsViewSet(viewsets.ModelViewSet):
    queryset = TournamentGameLogs.objects.all()
    serializer_class = TournamentGameLogsSerializer


class JoinTournamentGameViewSet(viewsets.ModelViewSet):
    queryset = JoinTournamentGame.objects.all()
    serializer_class = JoinTournamentGameSerializer
