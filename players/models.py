from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Nation(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Clan(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.description}"


class TankType(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Tank(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)
    type = models.ForeignKey(TankType, on_delete=models.CASCADE)
    tier = models.IntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f'{self.name} - {self.tier}'


class Player(models.Model):
    nickname = models.CharField(max_length=255, null=False, unique=True)
    clan = models.ForeignKey(Clan, on_delete=models.SET_NULL, null=True, blank=True)
    tanks = models.ManyToManyField(Tank, through='PlayerTank')

    def __str__(self):
        clan_name = self.clan.name if self.clan else 'No clan'
        return f'{self.nickname} - {clan_name}'


class PlayerTank(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    tank = models.ForeignKey(Tank, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player.nickname} - {self.tank.name}'
