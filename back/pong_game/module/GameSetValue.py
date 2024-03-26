from enum import Enum

FIELD_WIDTH: int = 1200
FIELD_LENGTH: int = 3000
PADDLE_WIDTH: int = 200
PADDLE_HEIGHT: int = 30
PADDLE_SPEED: int = 30
PADDLE_CORRECTION: int = 5
BALL_SPEED_X: int = 0
BALL_SPEED_Z: int = -10
BALL_RADIUS: int = 20
MAX_SCORE: int = 5


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
    SCORE = "score"
    END = "end"


class MessageType(Enum):
    READY = "ready"
    START = "start"
    PLAYING = "playing"
    SCORE = "score"
    END = "end"
    COMPLETE = "complete"
    ERROR = "error"


class GameTimeType(Enum):
    START_TIME = "start_time"
    END_TIME = "end_time"
