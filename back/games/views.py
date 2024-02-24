from django.db import IntegrityError
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]
    queryset = GeneralGameLogs.objects.all()
    serializer_class = GeneralGameLogsSerializer
    http_method_names = ["get", "post"]  # TODO debug를 위해 post 임시 추가

    # general game logs 생성 시 join general game 생성하는 오버라이딩 에러 발생
    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     JoinGeneralGame.objects.create(
    #         game_id=self.get_object().game_id,
    #         user_id=request.data["winner"],
    #     )
    #     JoinGeneralGame.objects.create(
    #         game_id=self.get_object().game_id,
    #         user_id=request.data["loser"],
    #     )

    def list(self, request, *args, **kwargs):
        # 밑에 if문은 debug를 위한 임시 get
        if "fk" not in kwargs:
            return super().list(request, *args, **kwargs)

        user_id = kwargs["fk"]
        # Q 객체는 복잡한 쿼리 조건을 사용할 때 사용, 밑에는 or 조건
        queryset = self.queryset.filter(Q(winner=user_id) | Q(loser=user_id))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class JoinGeneralGameViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = JoinGeneralGame.objects.all()
    serializer_class = JoinGeneralGameSerializer
    http_method_names = []

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:  # db의 무결성 제약 조건을 위반할 때 발생하는 에러
            raise ValidationError({"detail": "동일한 게임의 참가자가 이미 존재합니다."})


class TournamentGameLogsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TournamentGameLogs.objects.all()
    serializer_class = TournamentGameLogsSerializer
    http_method_names = ["get", "post"]  # TODO debug를 위해 post 임시 추가

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:  # db의 무결성 제약 조건을 위반할 때 발생하는 에러
            raise ValidationError({"detail": "동일한 게임이 이미 존재합니다."})

    def list(self, request, *args, **kwargs):
        # 밑에 if문은 debug를 위한 임시 get
        if "fk" not in kwargs and "name" not in kwargs:
            return super().list(request, *args, **kwargs)

        if "fk" in kwargs and "name" not in kwargs:
            user_id = kwargs["fk"]
            queryset = self.queryset.filter(Q(winner=user_id) | Q(loser=user_id))
        elif "name" in kwargs and "fk" not in kwargs:
            name = kwargs["name"]
            queryset = self.queryset.filter(tournament_name=name)
        else:
            raise ValidationError({"detail": "잘못된 요청입니다."})
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class JoinTournamentGameViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = JoinTournamentGame.objects.all()
    serializer_class = JoinTournamentGameSerializer
    http_method_names = []

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:  # db의 무결성 제약 조건을 위반할 때 발생하는 에러
            raise ValidationError({"detail": "동일한 게임의 참가자가 이미 존재합니다."})
