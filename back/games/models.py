import uuid
from django.db import models


class GeneralGameLogs(models.Model):
    game_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    winner = models.ForeignKey(
        "accounts.Users",
        on_delete=models.CASCADE,
        db_column="winner",
        related_name="general_winner",
    )
    loser = models.ForeignKey(
        "accounts.Users",
        on_delete=models.CASCADE,
        db_column="loser",
        related_name="general_loser",
    )

    class Meta:
        db_table = "GeneralGameLogs"
        ordering = ["start_time"]


class TournamentGameLogs(models.Model):
    tournament_name = models.CharField(max_length=20)
    round = models.IntegerField()
    winner = models.ForeignKey(
        "accounts.Users",
        on_delete=models.CASCADE,
        db_column="winner",
        related_name="tournament_winner",
    )
    loser = models.ForeignKey(
        "accounts.Users",
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
            models.UniqueConstraint(
                fields=["tournament_name", "round"], name="tournament_game_id"
            )
        ]
