from .Game import FIELD_LENGTH


class Paddle:
    def __init__(self):
        self.position_x: float = 0
        self.position_y: float = 0
        self.position_z: float = FIELD_LENGTH / 2
        self.width: float = 0
        self.speed: float = 0

    def reset_position(self):
        self.position_x = 0

    def left(self):
        self.position_x -= self.speed

    def right(self):
        self.position_x += self.speed

    def space(self):
        pass
