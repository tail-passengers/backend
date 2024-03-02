import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, DatabaseError
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from accounts.models import Users
from .serializers import (
    GeneralGameLogsSerializer,
    GeneralGameLogsListSerializer,
    TournamentGameLogsSerializer,
    TournamentGameLogsListSerializer,
    JoinGeneralGameSerializer,
    JoinTournamentGameSerializer,
)
from .models import (
    GeneralGameLogs,
    TournamentGameLogs,
    JoinGeneralGame,
    JoinTournamentGame,
)


def is_exist_user(key, value):
    try:
        user = None
        if key == "intra_id":
            user = Users.objects.get(intra_id=value)
        elif key == "user_id":
            uuid.UUID(value)  # UUID 형식인지 확인, 안하면 get 내부 함수에서 raise 발생
            user = Users.objects.get(user_id=value)
        return user
    except (ObjectDoesNotExist, ValueError):
        return None


def get_user_from_intra_id_or_user_id(ids):
    """
    intra_id 또는 user_id로 유저를 찾아 반환
    """
    user = is_exist_user("intra_id", ids)
    if user is None:
        user = is_exist_user("user_id", ids)
        if user is None:
            raise ValidationError({"error": "유저가 존재하지 않습니다."})
    return user


def create_with_intra_id_convert_to_user_id(self, request):
    """
    intra_id를 user_id로 변환하여 Game Log를 생성
    """
    winner_intra_id = request.data.get("winner")
    loser_intra_id = request.data.get("loser")

    winner_user = get_user_from_intra_id_or_user_id(winner_intra_id)
    loser_user = get_user_from_intra_id_or_user_id(loser_intra_id)

    request_copy_data = request.data.copy()
    request_copy_data["winner"] = winner_user.user_id
    request_copy_data["loser"] = loser_user.user_id

    serializer = self.get_serializer(data=request_copy_data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return (
        winner_user,
        loser_user,
        Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers),
    )


class GeneralGameLogsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = GeneralGameLogs.objects.all()
    serializer_class = GeneralGameLogsSerializer
    http_method_names = ["get", "post"]  # TODO debug를 위해 get 임시 추가

    # general game logs 생성 시 join general game 생성하는 오버라이딩 에러 발생
    # fk는 uuid가 아닌 인스턴스를 요구해서 생긴 에러인듯
    def create(self, request, *args, **kwargs):
        try:
            winner_user, loser_user, response = create_with_intra_id_convert_to_user_id(
                self, request
            )
            game_id = response.data["game_id"]
            if not game_id:
                return Response(
                    {"error": "Game이 존재하지 않습니다."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            game_instance = GeneralGameLogs.objects.get(game_id=game_id)
            JoinGeneralGame.objects.create(game_id=game_instance, user_id=winner_user)
            JoinGeneralGame.objects.create(game_id=game_instance, user_id=loser_user)
            return response

        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GeneralGameLogsListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = GeneralGameLogs.objects.all()
    serializer_class = GeneralGameLogsListSerializer

    def list(self, request, *args, **kwargs):
        # 밑에 if문은 debug를 위한 임시 get
        if "intra_id" not in kwargs:
            return super().list(request, *args, **kwargs)

        user = get_user_from_intra_id_or_user_id(kwargs["intra_id"])
        if user is None:
            return Response(
                {"error": "유저가 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
        queryset = self.queryset.filter(Q(winner=user.user_id) | Q(loser=user.user_id))
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
    http_method_names = ["get", "post"]  # TODO debug를 위해 get 임시 추가

    def create(self, request, *args, **kwargs):
        try:
            winner_user, loser_user, response = create_with_intra_id_convert_to_user_id(
                self, request
            )
            tournament_name = response.data["tournament_name"]
            if not tournament_name:
                return Response(
                    {"error": "Game이 존재하지 않습니다."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            game_instance = TournamentGameLogs.objects.get(
                tournament_name=tournament_name,
                round=response.data["round"],
            )
            JoinTournamentGame.objects.create(
                game_id=game_instance, user_id=winner_user
            )
            JoinTournamentGame.objects.create(game_id=game_instance, user_id=loser_user)
            return response

        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TournamentGameLogsListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TournamentGameLogs.objects.all()
    serializer_class = TournamentGameLogsListSerializer

    def list(self, request, *args, **kwargs):
        # 밑에 if문은 debug를 위한 임시 get
        if "intra_id" not in kwargs and "name" not in kwargs:
            return super().list(request, *args, **kwargs)

        if "intra_id" in kwargs and "name" not in kwargs:
            user = get_user_from_intra_id_or_user_id(kwargs["intra_id"])
            if user is None:
                return Response(
                    {"error": "유저가 존재하지 않습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            queryset = self.queryset.filter(
                Q(winner=user.user_id) | Q(loser=user.user_id)
            )
        elif "name" in kwargs and "intra_id" not in kwargs:
            queryset = self.queryset.filter(tournament_name=kwargs["name"])
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
