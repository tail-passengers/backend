from .GameSetValue import (
    PADDLE_SPEED,
    FIELD_WIDTH,
    PADDLE_WIDTH,
    FIELD_LENGTH,
    KeyboardInput,
)


class Paddle:
    def __init__(self, number: int):
        self.position_x: float = 0
        self.position_y: float = 0
        self.position_z: float = FIELD_LENGTH / 2 if number == 1 else -FIELD_LENGTH / 2

        self.left: bool = False
        self.right: bool = False

    def get_position_x(self) -> float:
        return self.position_x

    def input_handler(self, key_input: str) -> None:
        if key_input == KeyboardInput.LEFT_PRESS.value:
            self.left = True
        elif key_input == KeyboardInput.LEFT_RELEASE.value:
            self.left = False
        elif key_input == KeyboardInput.RIGHT_PRESS.value:
            self.right = True
        elif key_input == KeyboardInput.RIGHT_RELEASE.value:
            self.right = False

    def move_handler(self, player_num: int) -> None:
        if player_num == 1:
            if self.left and not self.right:
                self._move(-1)
            elif not self.left and self.right:
                self._move(1)
        elif player_num == 2:
            if self.left and not self.right:
                self._move(1)
            elif not self.left and self.right:
                self._move(-1)

    def _move(self, direction: int) -> None:
        new_paddle_x = self.position_x + direction * PADDLE_SPEED
        self.position_x = max(
            -FIELD_WIDTH / 2 + PADDLE_WIDTH / 2,
            min(FIELD_WIDTH / 2 - PADDLE_WIDTH / 2, new_paddle_x),
        )
