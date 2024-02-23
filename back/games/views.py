from django.db import IntegrityError
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
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
    http_method_names = ["get", "post"]  # TODO debug를 위해 post 임시 추가

    def list(self, request, *args, **kwargs):
        # 밑에 if문은 debug를 위한 임시 get
        if "fk" not in kwargs:
            return super().list(request, *args, **kwargs)

        user_id = kwargs["fk"]
        # Q 객체는 복잡한 쿼리 조건을 사용할 때 사용
        queryset = self.queryset.filter(Q(winner=user_id) | Q(loser=user_id))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


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
