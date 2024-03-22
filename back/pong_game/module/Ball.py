from .GameSetValue import FIELD_WIDTH, BALL_SPEED_X, BALL_SPEED_Z


class Ball:
    def __init__(self):
        self.position_x: float = 0
        self.position_y: float = 0
        self.position_z: float = 0
        self.radius: float = 20
        self.speed_x: float = BALL_SPEED_X
        self.speed_z: float = BALL_SPEED_Z

    def reset_position(self) -> None:
        self.position_x = 0
        self.position_y = 0
        self.position_z = 0
        self.speed_x = BALL_SPEED_X
        self.speed_z = BALL_SPEED_Z

    def update_ball_position(self) -> None:
        # TODO wasTouchingPaddle 들어갈 위치

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

    def get_position(self) -> tuple:
        return self.position_x, self.position_y, self.position_z

    def get_speed(self) -> tuple:
        return self.speed_x, self.speed_z
