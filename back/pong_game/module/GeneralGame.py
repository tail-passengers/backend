import json
from datetime import datetime

from .Player import Player
from .Ball import Ball
from .GameSetValue import (
    PlayerStatus,
    PADDLE_WIDTH,
    MessageType,
    GameTimeType,
    MAX_SCORE,
    GameStatus,
)


class GeneralGame:
    def __init__(self, player1: Player, player2: Player):
        self.__ball: Ball = Ball()
        self._player1: Player = player1
        self._player2: Player = player2
        self._score1: int = 0
        self._score2: int = 0
        self.__status: GameStatus = GameStatus.WAIT
        self.__start_time: Optional[datetime] = None
        self.__end_time: Optional[datetime] = None

    def is_all_ready(self) -> bool:
        if self.player1 is None or self.player2 is None:
        if self._player1 is None or self._player2 is None:
            return False
        if (
            self._player1.get_status()
            == self._player2.get_status()
            == PlayerStatus.READY
        ):
            return True
        return False

    def _is_past_paddle1(self) -> bool:
    def __is_past_paddle1(self) -> bool:
        return (
            self.__ball.position_z
            > self._player1.get_paddle().position_z + self.__ball.paddle_correction
        )

    def _is_past_paddle2(self) -> bool:
    def __is_past_paddle2(self) -> bool:
        return (
            self.__ball.position_z
            < self._player2.get_paddle().position_z - self.__ball.paddle_correction
        )

    def _is_paddle1_collision(self) -> bool:
    def __is_paddle1_collision(self) -> bool:
        return (
            self.__ball.position_z + self.__ball.radius
            >= self._player1.get_paddle().position_z
            and self.__is_ball_aligned_with_paddle(1)
        )

    def _is_paddle2_collision(self) -> bool:
    def __is_paddle2_collision(self) -> bool:
        return (
            self.__ball.position_z - self.__ball.radius
            <= self._player2.get_paddle().position_z
            and self.__is_ball_aligned_with_paddle(2)
        )

    def _is_ball_aligned_with_paddle(self, paddle_num: int) -> bool:
    def __is_ball_aligned_with_paddle(self, paddle_num: int) -> bool:
        half_paddle_width = PADDLE_WIDTH / 2
        paddle = (
            self._player1.get_paddle()
            if paddle_num == 1
            else self._player2.get_paddle()
        )
        return (
            paddle.position_x - half_paddle_width
            < self.__ball.position_x
            < paddle.position_x + half_paddle_width
        )

    def _reset_position(self) -> None:
        self.ball.reset_position()
    def __reset_position(self) -> None:
        self.__ball.reset_position()

    def key_input(self, text_data: json) -> None:
        data = json.loads(text_data)
        if data["input"] == "protego_maxima":
            self.__ball.protego_maxima()
        elif data["number"] == "player1":
            self._player1.paddle_handler(data["input"])
        elif data["number"] == "player2":
            self._player2.paddle_handler(data["input"])

    @staticmethod
    def build_ready_json(number: int, nickname: str) -> json:
        return json.dumps(
            {
                "message_type": MessageType.READY.value,
                "number": "player1" if number == 1 else "player2",
                "nickname": nickname,
            }
        )

    def build_start_json(self) -> json:
        return json.dumps(
            {
                "message_type": MessageType.START.value,
                "1p": self._player1.get_nickname(),
                "2p": self._player2.get_nickname(),
            }
        )

    def build_game_json(self, game_start: bool = True) -> json:
        self._move_paddle()
        self.__move_paddle()
        if game_start:
            self.__move_ball()
        paddle1 = self._player1.get_paddle().position_x
        paddle2 = self._player2.get_paddle().position_x
        ball_x, ball_y, ball_z = self.__ball.get_position()
        ball_vx, ball_vz = self.__ball.get_speed()
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
                "player1_score": self._score1,
                "player2_score": self._score2,
            }
        )

    def build_end_json(self) -> json:
        return json.dumps(
            {
                "message_type": MessageType.END.value,
                "winner": "player1" if self._score1 > self._score2 else "player2",
                "loser": "player2" if self._score1 > self._score2 else "player1",
            }
        )

    def build_error_json(self, nickname: str) -> json:
        self.status = GameStatus.END
        self.__status = GameStatus.END
        return json.dumps(
            {
                "message_type": MessageType.ERROR.value,
                "nickname": nickname,
            }
        )

    def build_complete_json(self, is_error=False) -> json:
        return json.dumps(
            {
                "message_type": (
                    MessageType.ERROR.value if is_error else MessageType.COMPLETE.value
                ),
                "winner": (
                    self._player1.get_nickname()
                    if self._score1 > self._score2
                    else self._player2.get_nickname()
                ),
                "loser": (
                    self._player2.get_nickname()
                    if self._score1 > self._score2
                    else self._player1.get_nickname()
                ),
            }
        )

    def _move_paddle(self) -> None:
        self.player1.get_paddle().move_handler(player_num=1)
        self.player2.get_paddle().move_handler(player_num=2)
    def __move_paddle(self) -> None:
        self._player1.get_paddle().move_handler(player_num=1)
        self._player2.get_paddle().move_handler(player_num=2)

    def _move_ball(self) -> None:
        self.ball.update_ball_position()
        if self._is_past_paddle1():
            self.score2 += 1
            self._reset_position()
            self.status = GameStatus.SCORE
        elif self._is_past_paddle2():
            self.score1 += 1
            self._reset_position()
            self.status = GameStatus.SCORE
        elif self.ball.is_side_collision():
            self.ball.speed_x *= -1
        elif self._is_paddle1_collision():
            self.ball.hit_ball_back(self.player1.get_paddle().get_position_x())
        elif self._is_paddle2_collision():
            self.ball.hit_ball_back(self.player2.get_paddle().get_position_x())
    def __move_ball(self) -> None:
        self.__ball.update_ball_position()
        if self.__is_past_paddle1():
            self._score2 += 1
            self.__reset_position()
            self.__status = GameStatus.SCORE
        elif self.__is_past_paddle2():
            self._score1 += 1
            self.__reset_position()
            self.__status = GameStatus.SCORE
        elif self.__ball.is_side_collision():
            self.__ball.speed_x = self.__ball.speed_x * -1
        elif self.__is_paddle1_collision():
            self.__ball.hit_ball_back(self._player1.get_paddle().position_x)
        elif self.__is_paddle2_collision():
            self.__ball.hit_ball_back(self._player2.get_paddle().position_x)

    def get_player(self, intra_id: str) -> tuple[Player, int] or None:
        if self.player1.intra_id == intra_id:
            return self.player1, 1
        elif self.player2.intra_id == intra_id:
            return self.player2, 2
        if self._player1.get_intra_id() == intra_id:
            return self._player1, 1
        elif self._player2.get_intra_id() == intra_id:
            return self._player2, 2
        return None

    def get_status(self) -> GameStatus:
        return self.status
        return self.__status

    def get_score(self) -> tuple:
        return self.score1, self.score2
        return self._score1, self._score2

    def get_ball_position(self) -> tuple:
        return self.ball.position_x, self.ball.position_z
        return self.__ball.position_x, self.__ball.position_z

    def get_ball_speed(self) -> tuple:
        return self.ball.speed_x, self.ball.speed_z
        return self.__ball.speed_x, self.__ball.speed_z

    def get_game_time(self, time_type: GameTimeType) -> datetime:
        if time_type == GameTimeType.START_TIME.value:
            return self.__start_time
        elif time_type == GameTimeType.END_TIME.value:
            return self.__end_time

    def set_game_time(self, time_type: GameTimeType) -> None:
        if time_type == GameTimeType.START_TIME.value:
            self.__start_time = datetime.now()
        elif time_type == GameTimeType.END_TIME.value:
            self.__end_time = datetime.now()

    def get_db_data(self) -> dict:
        return {
            "start_time": self.__start_time,
            "end_time": self.__end_time,
            "player1_intra_id": self._player1.get_intra_id(),
            "player2_intra_id": self._player2.get_intra_id(),
            "player1_score": self._score1,
            "player2_score": self._score2,
        }

    def get_winner_loser_intra_id(self) -> tuple:
        if self.score1 == MAX_SCORE:
            return self.player1.get_intra_id(), self.player2.get_intra_id()
        elif self.score2 == MAX_SCORE:
            return self.player2.get_intra_id(), self.player1.get_intra_id()
        if self._score1 == MAX_SCORE:
            return self._player1.get_intra_id(), self._player2.get_intra_id()
        elif self._score2 == MAX_SCORE:
            return self._player2.get_intra_id(), self._player1.get_intra_id()
        else:
            return None, None

    def set_player(self, player_intra_id: str, player_nickname: str) -> None:
        if self.player1 is None:
            self.player1 = Player(1, player_intra_id, player_nickname)
        if self._player1 is None:
            self._player1 = Player(1, player_intra_id, player_nickname)
            return

        if self._player2 is None:
            self._player2 = Player(2, player_intra_id, player_nickname)
            return

    def set_ready(self, number: str) -> None:
        if number == "player1":
            self._player1.set_status(PlayerStatus.READY)
        elif number == "player2":
            self._player2.set_status(PlayerStatus.READY)

    def set_status(self, status: GameStatus) -> None:
        self.status = status
        self.__status = status
