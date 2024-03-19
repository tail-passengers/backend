import json
from enum import Enum
from .Paddle import Paddle
from .Ball import Ball

FIELD_WIDTH: int = 1200
FIELD_LENGTH: int = 3000
PADDLE_WIDTH: int = 200
PADDLE_HEIGHT: int = 30
PADDLE_CORRECTION: int = 5


class KeyboardInput(Enum):
    LEFT = "left"
    RIGHT = "right"
    SPACE = "space"


class GeneralGame:
    def __init__(self, player1: str, player2: str):
        self.player1: str = player1
        self.player2: str = player2
        self.paddle1: Paddle = Paddle()
        self.paddle2: Paddle = Paddle()
        self.ball: Ball = Ball()
        self.score1: int = 0
        self.score2: int = 0

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
