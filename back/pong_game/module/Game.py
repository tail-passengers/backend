import json
from .Player import Player
from .Ball import Ball
from .GameSetValue import PlayerStatus


class GeneralGame:
    def __init__(self):
        self.ball: Ball = Ball()
        self.player1: Player | None = None
        self.player2: Player | None = None
        self.score1: int = 0
        self.score2: int = 0

    def set_player(self, player_intra_id: str) -> None:
        if self.player1 is None:
            self.player1 = Player(1, player_intra_id)
            return

        if self.player2 is None:
            self.player2 = Player(2, player_intra_id)
            return

    def get_player(self, number: int) -> Player | None:
        if number == 1:
            return self.player1
        elif number == 2:
            return self.player2
        return None

    def set_ready(self, number: str) -> None:
        if number == "player1":
            self.player1.set_status(PlayerStatus.READY)
        elif number == "player2":
            self.player2.set_status(PlayerStatus.READY)

    def get_ready(self) -> bool:
        if self.player1 is None or self.player2 is None:
            return False
        if self.player1.get_status() == self.player2.get_status() == PlayerStatus.READY:
            return True
        return False

    def reset_position(self) -> None:
        self.ball.reset_position()

    def key_input(self, text_data: json) -> None:
        data = json.loads(text_data)
        number = self.get_player(data["number"])
        if number == "1":
            self.player1.move_paddle(data["input"])
        elif number == "2":
            self.player2.move_paddle(data["input"])
