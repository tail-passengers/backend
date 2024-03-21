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

        # TODO front 구현에 따라 필요할 수도 안 필요할 수도 있음
        # self.direction: int = 1 if number == 1 else -1

    # TODO space 키는 프론트에서 처리 후, protego maxima 가 실행되었는지 판단하여 전달
    def key_handler(self, key_input: str) -> None:
        if key_input == KeyboardInput.LEFT_PRESS.value:
            self.left = True
        elif key_input == KeyboardInput.LEFT_RELEASE.value:
            self.left = False
        elif key_input == KeyboardInput.RIGHT_PRESS.value:
            self.right = True
        elif key_input == KeyboardInput.RIGHT_RELEASE.value:
            self.right = False

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
