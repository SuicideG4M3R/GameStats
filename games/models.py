from django.db import models
from players.models import Player
from django.core.validators import MinValueValidator, MaxValueValidator


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return f'Team {self.name} - {", ".join(player.nickname for player in self.players.all())}'


class Game(models.Model):
    date_played = models.DateTimeField(auto_now_add=True)
    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)

    def __str__(self):
        return f'Game {self.id} - {self.date_played}'


class GameResult(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    winner_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'Results for Game {self.game.id} - Winner Team: {self.winner_team}'
