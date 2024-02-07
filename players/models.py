from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Nation(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Clan(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('clan_detail', args=(self.id,))

    def __str__(self):
        return self.name


class TankType(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Tank(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    type = models.ForeignKey(TankType, on_delete=models.CASCADE)
    tier = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def get_absolute_url(self):
        return reverse('tank_detail', args=(self.id,))

    def __str__(self):
        return f'Tank: {self.name} - {self.tier} tier {self.nation}'


class Player(models.Model):
    nickname = models.CharField(max_length=255, null=False, unique=True)
    clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, null=True, blank=True)
    tanks = models.ManyToManyField(Tank, through='PlayerTank')

    def get_absolute_url(self):
        return reverse('player_detail', args=(self.id,))

    def __str__(self):
        clan_name = self.clan.name if self.clan else 'No Clan'
        return f'{self.nickname} [{clan_name}]'


class PlayerTank(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player.nickname} - {self.tank.name}'


class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    players = models.ManyToManyField(Player)

    def get_absolute_url(self):
        return reverse('team_detail', args=(self.id,))

    def __str__(self):
        return f'{self.name} - {", ".join(player.nickname for player in self.players.all())}'


class Game(models.Model):
    date_played = models.DateTimeField(auto_now_add=True)
    team1 = models.ForeignKey(Team, related_name='team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2', on_delete=models.CASCADE)

    def __str__(self):
        return f'Game {self.id} - {self.date_played}'


class GameResult(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    winner_team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('game_detail', args=(self.id,))

    def __str__(self):
        team1_name = self.game.team1.name if self.game.team1 else 'Team 1'
        team2_name = self.game.team2.name if self.game.team2 else 'Team 2'

        result_str = f'{self.game.date_played.date()} {team1_name} vs {team2_name}'

        if self.winner_team:
            winner_name = self.winner_team.name
            result_str += f' --> {winner_name}'

        return result_str
