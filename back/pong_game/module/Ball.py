from .Game import FIELD_WIDTH


class Ball:
    def __init__(self):
        self.position_x: float = 0
        self.position_y: float = 0
        self.position_z: float = 0
        self.radius: float = 20
        self.speed_x: float = 0
        self.speed_z: float = 0

    def reset_position(self) -> None:
        self.position_x = 0
        self.position_y = 0
        self.position_z = 0
        self.speed_x = 0
        self.speed_z = 0

    def move(self) -> None:
        # TODO 충돌 여부에 대한 로직도 프론트엔 있음

        self.position_x += self.speed_x
        self.position_z += self.speed_z
        self.position_y = -((self.position_z - 1) * (self.position_z - 1) / 5000) + 435

    def is_side_collision(self) -> bool:
        half_field_width = (FIELD_WIDTH - 2) / 2
        return (
            self.position_x - self.radius < -half_field_width
            or self.position_x + self.radius > half_field_width
        )

    def hit_ball_back(self, paddle_x: float) -> None:
        self.speed_x = (self.position_x - paddle_x) / 9
        self.speed_z *= -1

    def protego_maxima(self) -> None:
        self.radius += 5
        self.speed_z += 1
