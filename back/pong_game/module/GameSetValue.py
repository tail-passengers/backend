from enum import Enum

FIELD_WIDTH: int = 1200
FIELD_LENGTH: int = 3000
PADDLE_WIDTH: int = 200
PADDLE_HEIGHT: int = 30
PADDLE_CORRECTION: int = 5


class KeyboardInput(Enum):
    LEFT = "left"
    RIGHT = "right"
    SPACE = "space"
