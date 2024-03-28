import json

from .GameSetValue import (
    TournamentStatus,
    MessageType,
    PlayerNumber,
    TOURNAMENT_PLAYER_MAX_CNT,
    PlayerStatus,
    TournamentGroupName,
    RoundNumber,
)
from .Player import Player
from .Round import Round


class Tournament:
    def __init__(self, tournament_name: str, create_user_intra_id: str):
        self.tournament_name: str = tournament_name
        self.round_list: list[Round or None] = [None, None, None]
        self.player_list: list[Player or None] = [
            Player(number=1, intra_id=create_user_intra_id),
            None,
            None,
            None,
        ]
        self.player_total_cnt: int = 1
        self.status: TournamentStatus = TournamentStatus.WAIT

    def build_tournament_wait_dict(self) -> dict:
        return {
            "tournament_name": self.tournament_name,
            "wait_num": str(self.player_total_cnt),
        }

    def _join_tournament_with_intra_id(self, intra_id: str) -> PlayerNumber:
        for idx, player in enumerate(self.player_list):
            if player.get_intra_id() == intra_id:
                return PlayerNumber.PLAYER_1
            elif player is None:
                self.player_list[idx] = Player(number=idx + 1, intra_id=intra_id)
                self.player_total_cnt += 1
                if self.player_total_cnt == TOURNAMENT_PLAYER_MAX_CNT:
                    self.status = TournamentStatus.READY
                return list(PlayerNumber)[idx]

    def build_tournament_wait_detail_json(self, intra_id: str) -> tuple[str, json]:
        player_number = self._join_tournament_with_intra_id(intra_id=intra_id).value
        return player_number, json.dumps(
            {
                "message_type": MessageType.WAIT.value,
                "intra_id": intra_id,
                "total": self.player_total_cnt,
                "number": player_number,
            }
        )

    def build_tournament_ready_json(self, team_name: TournamentGroupName) -> json:
        if team_name == TournamentGroupName.A_TEAM:
            return json.dumps(
                {
                    "message_type": MessageType.READY.value,
                    "round": RoundNumber.ROUND_1.value,
                    "1p": self.player_list[0].get_intra_id(),
                    "2p": self.player_list[1].get_intra_id(),
                }
            )
        else:
            return json.dumps(
                {
                    "message_type": MessageType.READY.value,
                    "round": RoundNumber.ROUND_2.value,
                    "1p": self.player_list[2].get_intra_id(),
                    "2p": self.player_list[3].get_intra_id(),
                }
            )

    def disconnect_tournament(self, intra_id: str) -> None:
        for idx, player in enumerate(self.player_list):
            if player.get_intra_id() == intra_id:
                self.player_list[idx] = None
                self.player_total_cnt -= 1

    def is_all_ready(self) -> bool:
        for player in self.player_list:
            if player is None:
                return False
            if player.get_status() != PlayerStatus.READY:
                return False

        return True

    def get_statue(self) -> TournamentStatus:
        return self.status

    def get_player_total_cnt(self) -> int:
        return self.player_total_cnt

    def try_set_ready(self, player_number: PlayerNumber, intra_id: str) -> bool:
        idx = list(PlayerNumber).index(player_number)
        if (
            self.player_list[idx] is None
            or self.player_list[idx].get_intra_id() != intra_id
        ):
            return False
        self.player_list[idx].set_status(PlayerStatus.READY)
        return True
