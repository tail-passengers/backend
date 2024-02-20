import uuid
from django.db import models


class JoinGeneralGame(models.Model):
    game_id = models.ForeignKey(
        "GeneralGameLogs",
        on_delete=models.CASCADE,
        db_column="game_id",
    )
    user_id = models.ForeignKey(
        "users.Users",
        on_delete=models.CASCADE,
        db_column="user_id",
    )

    class Meta:
        db_table = "JoinGeneralGame"
        constraints = [
            models.UniqueConstraint(fields=['game_id', 'user_id'], name='join_general_game_id')
        ]


class GeneralGameLogs(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    winner = models.ForeignKey(
        "users.Users",
        on_delete=models.CASCADE,
        db_column="winner",
        related_name="general_winner",
    )
    loser = models.ForeignKey(
        "users.Users",
        on_delete=models.CASCADE,
        db_column="loser",
        related_name="general_loser",
    )

    class Meta:
        db_table = "GeneralGameLogs"
        ordering = ["start_time"]


class JoinTournamentGame(models.Model):
    game_id = models.ForeignKey(
        "TournamentGameLogs",
        on_delete=models.CASCADE,
        db_column="game_id",
    )
    user_id = models.ForeignKey(
        "users.Users",
        on_delete=models.CASCADE,
        db_column="user_id",
    )

    class Meta:
        db_table = "JoinTournamentGame"
        constraints = [
            models.UniqueConstraint(fields=['game_id', 'user_id'], name='join_tournament_game_id')
        ]


class TournamentGameLogs(models.Model):
    tournament_name = models.CharField(max_length=20)
    round = models.IntegerField()
    winner = models.ForeignKey(
        "users.Users",
        on_delete=models.CASCADE,
        db_column="winner",
        related_name="tournament_winner",
    )
    loser = models.ForeignKey(
        "users.Users",
        on_delete=models.CASCADE,
        db_column="loser",
        related_name="tournament_loser",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_final = models.BooleanField()

    class Meta:
        db_table = "TournamentGameLogs"
        ordering = ["start_time"]
        constraints = [
            models.UniqueConstraint(fields=['tournament_name', 'round'], name='tournament_game_id')
        ]
