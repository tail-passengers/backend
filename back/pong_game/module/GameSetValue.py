from enum import Enum

FIELD_WIDTH: int = 1200
FIELD_LENGTH: int = 3000
PADDLE_WIDTH: int = 200
PADDLE_HEIGHT: int = 30
PADDLE_SPEED: int = 30
PADDLE_CORRECTION: int = 5


class KeyboardInput(Enum):
    LEFT_PRESS = "left_press"
    LEFT_RELEASE = "left_release"
    RIGHT_PRESS = "right_press"
    RIGHT_RELEASE = "right_release"
    SPACE = "space"


class PlayerStatus(Enum):
    WAIT = "wait"
    READY = "ready"
    PLAYING = "playing"
    WIN = "win"
    LOSE = "lose"
