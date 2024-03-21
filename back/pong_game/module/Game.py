import json
from .Paddle import Paddle
from .Ball import Ball
from .GameSetValue import PADDLE_CORRECTION, KeyboardInput


class GeneralGame:
    def __init__(self):
        self.player1: str | None = None
        self.player2: str | None = None
        self.paddle1: Paddle = Paddle()
        self.paddle2: Paddle = Paddle()
        self.ball: Ball = Ball()
        self.score1: int = 0
        self.score2: int = 0

    def set_player(self, player_intra_id: str) -> None:
        if self.player1 is None:
            self.player1 = player_intra_id
            return

        if self.player2 is None:
            self.player2 = player_intra_id
            return

    def get_player(self, player_id: int) -> str | None:
        if player_id == 1:
            return self.player1
        elif player_id == 2:
            return self.player2
        return None

    def reset_position(self) -> None:
        self.paddle1.reset_position()
        self.paddle2.reset_position()
        self.ball.reset_position()

    def update_position(self, text_data: json) -> None:
        data = json.load(text_data)
        if data["intra_id"] == self.player1:
            if data["keyboard_input"] == KeyboardInput.LEFT:
                self.paddle1.left()
            elif data["keyboard_input"] == KeyboardInput.RIGHT:
                self.paddle1.right()
            elif data["keyboard_input"] == KeyboardInput.SPACE:
                self.paddle1.space()
        elif data["intra_id"] == self.player2:
            if data["keyboard_input"] == KeyboardInput.LEFT:
                self.paddle2.left()
            elif data["keyboard_input"] == KeyboardInput.RIGHT:
                self.paddle2.right()
            elif data["keyboard_input"] == KeyboardInput.SPACE:
                self.paddle2.space()

    def is_past_paddle(self, intra_id: str) -> bool:
        if intra_id == self.player1:
            return self.ball.position_z > self.paddle1.position_z + PADDLE_CORRECTION
        elif intra_id == self.player2:
            return self.ball.position_z < self.paddle2.position_z - PADDLE_CORRECTION
        return False
