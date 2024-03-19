from .Game import FIELD_WIDTH


class Ball:
    def __init__(self):
        self.position_x: int = 0
        self.position_y: int = 0
        self.position_z: int = 0
        self.radius: int = 20
        self.speed_x: int = 0
        self.speed_z: int = 0

    def reset_position(self):
        self.position_x = 0
        self.position_y = 0
        self.position_z = 0
        self.speed_x = 0
        self.speed_z = 0

    def move(self):
        # TODO 충돌 여부에 대한 로직도 프론트엔 있음

        self.position_x += self.speed_x
        self.position_z += self.speed_z
        self.position_y = -((self.position_z - 1) * (self.position_z - 1) / 5000) + 435

    def is_side_collision(self):
        half_field_width = (FIELD_WIDTH - 2) / 2
        return (
            self.position_x - self.radius < -half_field_width
            or self.position_x + self.radius > half_field_width
        )

    def hit_ball_back(self, paddle_x: int):
        self.speed_x = (self.position_x - paddle_x) / 9
        self.speed_z *= -1

    def protego_maxima(self):
        self.radius += 5
        self.speed_z += 1
