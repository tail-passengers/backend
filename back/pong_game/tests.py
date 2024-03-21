import json
import uuid

from back.asgi import (
    application,
)

from django.test import TestCase
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from accounts.models import Users, UserStatusEnum


class LoginConsumerTests(TestCase):
    @database_sync_to_async
    def create_test_user(self, intra_id):
        # 테스트 사용자 생성
        return get_user_model().objects.create_user(intra_id=intra_id)

    @database_sync_to_async
    def delete_test_user(self, user):
        # 테스트 사용자 삭제
        user.delete()

    @database_sync_to_async
    def get_user_status(self, user):
        # 데이터베이스에서 사용자 상태 조회
        return Users.objects.get(user_id=user.user_id).status

    async def test_authenticated_user_connection(self):
        """
        인증된 유저의 경우 접속 테스트
        """
        self.user = await self.create_test_user(intra_id="1")
        communicator = WebsocketCommunicator(application, "/ws/login/")
        # user 인증
        communicator.scope["user"] = self.user

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        user_status = await self.get_user_status(self.user)
        self.assertEqual(user_status, UserStatusEnum.ONLINE)

        # 연결 해제 및 상태 확인
        await communicator.disconnect()
        user_status = await self.get_user_status(self.user)
        self.assertEqual(user_status, UserStatusEnum.OFFLINE)

    async def test_unauthenticated_user_connection(self):
        """
        인증이 되지 않는 유저의 경우 접속 테스트
        """
        communicator = WebsocketCommunicator(application, "/ws/login/")

        connected, _ = await communicator.connect()
        self.assertFalse(connected)


class GeneralGameWaitConsumerTests(TestCase):
    @database_sync_to_async
    def create_test_user(self, intra_id):
        # 테스트 사용자 생성
        return get_user_model().objects.create_user(intra_id=intra_id)

    @database_sync_to_async
    def delete_test_user(self, user):
        # 테스트 사용자 삭제
        user.delete()

    async def test_authenticated_user_connection(self):
        """
        2명 접속시 game_id, player1, 2 인트라 아이디 받는지 확인
        """
        self.user1 = await self.create_test_user(intra_id="test1")
        self.user2 = await self.create_test_user(intra_id="test2")
        communicator1 = WebsocketCommunicator(application, "/ws/general_game/wait/")
        # user 인증
        communicator1.scope["user"] = self.user1
        # 접속 확인
        connected, _ = await communicator1.connect()
        self.assertTrue(connected)

        communicator2 = WebsocketCommunicator(application, "/ws/general_game/wait/")
        communicator2.scope["user"] = self.user2
        # 접속 확인
        connected, _ = await communicator2.connect()
        self.assertTrue(connected)

        # user1 응답 확인
        user1_response = await communicator1.receive_from()
        user1_response_dict = json.loads(user1_response)

        # user2 응답 확인
        user2_response = await communicator2.receive_from()
        user2_response_dict = json.loads(user2_response)

        # game_id 동일 한지 확인
        self.assertEqual(user1_response_dict["game_id"], user2_response_dict["game_id"])


class GeneralGameConsumerTests(TestCase):
    @database_sync_to_async
    def create_test_user(self, intra_id):
        # 테스트 사용자 생성
        return get_user_model().objects.create_user(intra_id=intra_id)

    @database_sync_to_async
    def delete_test_user(self, user):
        # 테스트 사용자 삭제
        user.delete()

    async def test_authenticated_user_connection(self):
        """
        두 명 접속시 message_type 잘 보내는지 확인
        """
        self.user1 = await self.create_test_user(intra_id="test1")
        self.user2 = await self.create_test_user(intra_id="test2")
        self.game_id = str(uuid.uuid4())
        communicator1 = WebsocketCommunicator(
            application, f"/ws/general_game/{self.game_id}/"
        )

        # user 인증
        communicator1.scope["user"] = self.user1
        # 접속 확인
        connected, _ = await communicator1.connect()
        self.assertTrue(connected)

        # user1 응답 확인
        user1_response = await communicator1.receive_from()
        user1_response_dict = json.loads(user1_response)
        self.assertEqual(user1_response_dict["message_type"], "ready")
        self.assertEqual(user1_response_dict["intra_id"], self.user1.intra_id)
        self.assertEqual(user1_response_dict["number"], "player1")

        communicator2 = WebsocketCommunicator(
            application, f"/ws/general_game/{self.game_id}/"
        )
        # user 인증
        communicator2.scope["user"] = self.user2
        # 접속 확인
        connected, _ = await communicator2.connect()
        self.assertTrue(connected)

        # user2 응답 확인
        user2_response = await communicator2.receive_from()
        user2_response_dict = json.loads(user2_response)
        self.assertEqual(user2_response_dict["message_type"], "ready")
        self.assertEqual(user2_response_dict["intra_id"], self.user2.intra_id)
        self.assertEqual(user2_response_dict["number"], "player2")

        # user1,2 응답
        await communicator1.send_to(text_data=user1_response)
        await communicator2.send_to(text_data=user2_response)

        # user1, user2 start 메시지 확인
        user1_second_response = await communicator1.receive_from()
        user1_second_dict = json.loads(user1_second_response)
        self.assertEqual(user1_second_dict["message_type"], "start")
        self.assertEqual(user1_second_dict["1p"], self.user1.intra_id)
        self.assertEqual(user1_second_dict["2p"], self.user2.intra_id)

        user2_second_response = await communicator2.receive_from()
        user2_second_dict = json.loads(user2_second_response)
        self.assertEqual(user2_second_dict["message_type"], "start")
        self.assertEqual(user2_second_dict["1p"], self.user1.intra_id)
        self.assertEqual(user2_second_dict["2p"], self.user2.intra_id)
