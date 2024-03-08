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
