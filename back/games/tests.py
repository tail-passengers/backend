from django.utils.timezone import make_aware
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import GeneralGameLogs, JoinGeneralGame
import pytz
from datetime import datetime
from accounts.models import Users


class GeneralGameLogsViewSetTest(APITestCase):
    def setUp(self):
        # 두 명의 사용자 생성
        self.user1 = Users.objects.create_user(intra_id="user1")
        self.user2 = Users.objects.create_user(intra_id="user2")
        # 게임 로그 URL
        self.create_url = reverse("general_game_logs")
        self.list_url = reverse("general_game_logs")

    def test_create_general_game_log_without_authenticate(self):
        """
        인증이 없을때 403 에러 확인
        """
        data = {
            "start_time": "2021-01-01T00:00:00Z",
            "end_time": "2021-01-01T01:00:00Z",
            "winner": self.user1.user_id,
            "loser": self.user2.user_id,
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_general_game_log_wit_authenticate(self):
        """
        인증이 있을때 201 상태 코드 확인
        """
        self.client.force_authenticate(user=self.user1)
        tz = pytz.timezone("Asia/Seoul")  # 서울 시간대(UTC+9) 설정
        start_time = make_aware(datetime(2021, 1, 1, 0, 0, 0), timezone=tz)
        end_time = make_aware(datetime(2021, 1, 2, 1, 0, 0), timezone=tz)
        winner = self.user1.user_id
        loser = self.user2.user_id
        data = {
            "start_time": start_time,
            "end_time": end_time,
            "winner": winner,
            "loser": loser,
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # GeneralGameLogs 모델에서 데이터가 잘 들어갔는지 확인
        game_log = GeneralGameLogs.objects.get(game_id=response.data["game_id"])
        self.assertEqual(game_log.start_time, start_time)
        self.assertEqual(game_log.end_time, end_time)
        self.assertEqual(game_log.winner.user_id, winner)
        self.assertEqual(game_log.loser.user_id, loser)

        # JoinGeneralGame 모델에 게임 로그가 생성 되었는지 확인
        self.assertTrue(JoinGeneralGame.objects.filter(user_id=self.user1).exists())
        game_log = JoinGeneralGame.objects.get(user_id=self.user1)
        self.assertEqual(game_log.game_id, response.data["game_id"])
        self.assertTrue(JoinGeneralGame.objects.filter(user_id=self.user2).exists())
        game_log = JoinGeneralGame.objects.get(user_id=self.user2)
        self.assertEqual(game_log.game_id, response.data["game_id"])
