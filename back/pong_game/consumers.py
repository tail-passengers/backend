import json
import uuid
from enum import Enum
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import Users, UserStatusEnum
from collections import deque
from .module.Game import GeneralGame


class MessageType(Enum):
    READY = "ready"
    START = "start"
    PLAYING = "playing"
    END = "end"


class LoginConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user: Users = None

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
            await self.update_user_status(UserStatusEnum.ONLINE)
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.update_user_status(UserStatusEnum.OFFLINE)

    @database_sync_to_async
    def update_user_status(self, status):
        Users.objects.filter(user_id=self.user.user_id).update(status=status)


class GeneralGameWaitConsumer(AsyncWebsocketConsumer):
    intra_id_list, wait_list = list(), deque()

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user: Users = None

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated and await self.add_wait_list():
            await self.accept()
            if len(GeneralGameWaitConsumer.wait_list) > 1:
                await GeneralGameWaitConsumer.game_match()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            if (
                self in GeneralGameWaitConsumer.wait_list
                and self.user.intra_id in GeneralGameWaitConsumer.intra_id_list
            ):
                GeneralGameWaitConsumer.intra_id_list.remove(self.user.intra_id)
                GeneralGameWaitConsumer.wait_list.remove(self)

    @classmethod
    async def game_match(cls):
        game_id = str(uuid.uuid4())
        player1 = GeneralGameWaitConsumer.wait_list.popleft()
        player2 = GeneralGameWaitConsumer.wait_list.popleft()
        await player1.send(json.dumps({"game_id": game_id}))
        await player2.send(json.dumps({"game_id": game_id}))
        GeneralGameWaitConsumer.intra_id_list.remove(player1.user.intra_id)
        GeneralGameWaitConsumer.intra_id_list.remove(player2.user.intra_id)

    async def add_wait_list(self):
        if self.user.intra_id in GeneralGameWaitConsumer.intra_id_list:
            return False
        GeneralGameWaitConsumer.wait_list.append(self)
        GeneralGameWaitConsumer.intra_id_list.append(self.user.intra_id)
        return True


# TODO url game_id 유효한지? 동일한지? 확인 로직 필요?
class GeneralGameConsumer(AsyncWebsocketConsumer):
    active_games: dict[str, GeneralGame] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user: Users = None
        self.game_id: str | None = None
        self.game_group_name: str | None = None

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
            self.game_group_name = f"game_{self.game_id}"
            await self.channel_layer.group_add(self.game_group_name, self.channel_name)
            await self.accept()
            if self.game_id not in GeneralGameConsumer.active_games.keys():
                game = GeneralGame()
                game.set_player(self.user.intra_id)
                GeneralGameConsumer.active_games[self.game_id] = game
                await self.send(
                    json.dumps(
                        {
                            "message_type": MessageType.READY.value,
                            "intra_id": self.user.intra_id,
                            "number": "player1",
                        }
                    )
                )
            else:
                GeneralGameConsumer.active_games[self.game_id].set_player(
                    self.user.intra_id
                )
                await self.send(
                    json.dumps(
                        {
                            "message_type": MessageType.READY.value,
                            "intra_id": self.user.intra_id,
                            "number": "player2",
                        }
                    )
                )
                await self.channel_layer.group_send(
                    self.game_group_name,
                    {
                        "type": "game.message",
                        "message": json.dumps(
                            {
                                "message_type": MessageType.START.value,
                                "1p": GeneralGameConsumer.active_games[
                                    self.game_id
                                ].get_player(1),
                                "2p": self.user.intra_id,
                            }
                        ),
                    },
                )

        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.game_group_name, self.channel_name
            )

    async def game_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=message)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
