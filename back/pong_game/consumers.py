from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import Users, UserStatusEnum


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


class GeneralGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
            self.game_group_name = f"game_{self.game_id}"
            await self.channel_layer.group_add(self.game_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.game_group_name, self.channel_name
            )

    async def receive(self, text_data):
        # 게임 로직 추가 필요
        pass
