import asyncio
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import Users, UserStatusEnum
from collections import deque


class LoginConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
            await self.update_user_status(self.user, UserStatusEnum.ONLINE)
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.update_user_status(self.user, UserStatusEnum.OFFLINE)

    @database_sync_to_async
    def update_user_status(self, user, status):
        Users.objects.filter(user_id=user.user_id).update(status=status)


class GeneralGameWaitConsumer(AsyncWebsocketConsumer):
    intra_id_list, wait_list = set(), deque()

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated and await self.add_wait_list(self):
            await self.accept()
            await self.wait_queue()
        else:
            await self.close()

    @classmethod
    async def wait_queue(cls):
        while True:
            if len(cls.wait_list) > 1:
                game_id = str(uuid.uuid4())
                player1 = cls.wait_list.popleft()
                player2 = cls.wait_list.popleft()
                await player1.send(game_id)
                await player2.send(game_id)
                cls.intra_id_list.remove(player1.user.intra_id)
                cls.intra_id_list.remove(player2.user.intra_id)
            await asyncio.sleep(1)

    @classmethod
    async def add_wait_list(cls, self):
        if self.user.intra_id in cls.intra_id_list:
            return False
        cls.wait_list.append(self)
        cls.intra_id_list.add(self.user.intra_id)
        return True
