import json
from .Player import Player
from .Ball import Ball
from .GameSetValue import PlayerStatus, PADDLE_CORRECTION, PADDLE_WIDTH, MessageType


class GeneralGame:
    def __init__(self):
        self.ball: Ball = Ball()
        self.player1: Player | None = None
        self.player2: Player | None = None
        self.score1: int = 0
        self.score2: int = 0
        self.status: PlayerStatus = PlayerStatus.WAIT

    def is_all_ready(self) -> bool:
        if self.player1 is None or self.player2 is None:
            return False
        if self.player1.get_status() == self.player2.get_status() == PlayerStatus.READY:
            return True
        return False

    def _is_past_paddle1(self) -> bool:
        return self.ball.position_z > self.player1.paddle.position_z + PADDLE_CORRECTION


    def _is_past_paddle2(self) -> bool:
        return self.ball.position_z < self.player2.paddle.position_z - PADDLE_CORRECTION

    def _is_paddle1_collision(self) -> bool:
        return (
            self.ball.position_z + self.ball.radius >= self.player1.paddle.position_z
            and self._is_ball_aligned_with_paddle(1)
        )

    def _is_paddle2_collision(self) -> bool:
        return (
            self.ball.position_z - self.ball.radius <= self.player2.paddle.position_z
            and self._is_ball_aligned_with_paddle(2)
        )

    def _is_ball_aligned_with_paddle(self, paddle_num: int) -> bool:
        half_paddle_width = PADDLE_WIDTH / 2
        paddle = self.player1.paddle if paddle_num == 1 else self.player2.paddle
        return self.ball.position_x > paddle.position_x - half_paddle_width

    def _reset_position(self) -> None:
        self.ball.reset_position()

    def key_input(self, text_data: json) -> None:
        data = json.loads(text_data)
        if data["number"] == "player1":
            self.player1.paddle_handler(data["input"])
        elif data["number"] == "player2":
            self.player2.paddle_handler(data["input"])

    def build_start_json(self) -> json:
        return json.dumps(
            {
                "message_type": MessageType.START.value,
                "1p": self.player1.get_intra_id(),
                "2p": self.player2.get_intra_id(),
            }
        )

    def build_game_json(self) -> json:
        self._move_paddle()
        self._move_ball()
        paddle1 = self.player1.get_paddle().get_position_x()
        paddle2 = self.player2.get_paddle().get_position_x()
        ball_x, ball_y, ball_z = self.ball.get_position()
        ball_vx, ball_vz = self.ball.get_speed()
        return json.dumps(
            {
                "message_type": MessageType.PLAYING.value,
                "paddle1": paddle1,
                "paddle2": paddle2,
                "ball_x": ball_x,
                "ball_y": ball_y,
                "ball_z": ball_z,
                "ball_vx": ball_vx,
                "ball_vz": ball_vz,
            }
        )

    def build_score_json(self) -> json:
        return json.dumps(
            {
                "message_type": MessageType.SCORE.value,
                "player1_score": self.score1,
                "player2_score": self.score2,
            }
        )

    def build_end_json(self) -> json:
        return json.dumps(
            {
                "message_type": MessageType.END.value,
                "winner": "player1" if self.score1 > self.score2 else "player2",
                "loser": "player2" if self.score1 > self.score2 else "player1",
            }
        )

    def _move_paddle(self) -> None:
        self.player1.get_paddle().move_handler()
        self.player2.get_paddle().move_handler()

    def _move_ball(self) -> None:
        self.ball.update_ball_position()
        if self._is_past_paddle1():
            self.score2 += 1
            self._reset_position()
            self.status = PlayerStatus.SCORE
        elif self._is_past_paddle2():
            self.score1 += 1
            self._reset_position()
            self.status = PlayerStatus.SCORE
        elif self.ball.is_side_collision():
            self.ball.speed_x *= -1
        elif self._is_paddle1_collision():
            self.ball.hit_ball_back(self.player1.get_paddle().get_position_x())
        elif self._is_paddle2_collision():
            self.ball.hit_ball_back(self.player2.get_paddle().get_position_x())

    def get_player(self, number: int) -> Player | None:
        if number == 1:
            return self.player1
        elif number == 2:
            return self.player2
        return None

    def get_status(self) -> PlayerStatus:
        return self.status

    def get_score(self) -> tuple:
        return self.score1, self.score2

    def get_ball_position(self) -> tuple:
        return self.ball.position_x, self.ball.position_z

    def get_ball_speed(self) -> tuple:
        return self.ball.speed_x, self.ball.speed_z

    def set_player(self, player_intra_id: str) -> None:
        if self.player1 is None:
            self.player1 = Player(1, player_intra_id)
            return

        if self.player2 is None:
            self.player2 = Player(2, player_intra_id)
            return

    def set_ready(self, number: str) -> None:
        if number == "player1":
            self.player1.set_status(PlayerStatus.READY)
        elif number == "player2":
            self.player2.set_status(PlayerStatus.READY)

    def set_status(self, status: PlayerStatus) -> None:
        self.status = status
