from datetime import datetime

import pytest
from django.contrib.auth.models import User, Group, Permission

from players.models import *


@pytest.fixture
def my_user():
    return User.objects.create_user(username='Jarosław', password='12345678')


@pytest.fixture
def my_superuser():
    return User.objects.create_superuser(username='Jarosław', password='12345678')


@pytest.fixture
def my_user_with_permissions():
    user = User.objects.create_user(username='Jarosław', password='12345678')
    group = Group.objects.create(name='Group 1')
    group.permissions.set(Permission.objects.all())
    user.groups.add(group)
    return user


@pytest.fixture
def complete_data():
    clan2 = Clan.objects.create(name='Clan1', description='Description1')
    player2 = Player.objects.create(nickname='Player1', clan_id=clan2.id)
    team1 = Team.objects.create(name='Team1')
    team2 = Team.objects.create(name='Team2')
    tank_type2 = TankType.objects.create(name='TankType1')
    nation2 = Nation.objects.create(name='Nation1')
    tank2 = Tank.objects.create(name='Tank1', nation_id=nation2.id, type_id=tank_type2.id, tier=8)
    player_tank2 = PlayerTank.objects.create(player_id=player2.id, tank_id=tank2.id)
    team1.players.add(player2)
    team2.players.add(player2)
    game2 = Game.objects.create(date_played=datetime.now(), team1_id=team1.id, team2_id=team2.id)
    game_result2 = GameResult.objects.create(game_id=game2.id, winner_team_id=team1.id)
    return clan2, player2, team1, team2, tank_type2, nation2, tank2, player_tank2, game2, game_result2


@pytest.fixture
def clan():
    return Clan.objects.create(name='Clan1', description='Description1')


@pytest.fixture
def clans():
    data = [Clan.objects.create(name='Clan1', description='Description1'),
            Clan.objects.create(name='Clan2', description='Description2'),
            Clan.objects.create(name='Clan3', description='Description3'),
            Clan.objects.create(name='Clan4', description='Description4'),
            Clan.objects.create(name='Clan5', description='Description5'),
            Clan.objects.create(name='Clan6', description='Description6'),
            Clan.objects.create(name='Clan7', description='Description7'),
            ]
    return data


@pytest.fixture
def player(clan):
    return Player.objects.create(nickname='Player1', clan_id=clan.id)


@pytest.fixture
def players(clan):
    data = [Player.objects.create(nickname='Player1', clan_id=clan.id),
            Player.objects.create(nickname='Player2', clan_id=clan.id),
            Player.objects.create(nickname='Player3', clan_id=clan.id),
            Player.objects.create(nickname='Player4', clan_id=clan.id),
            Player.objects.create(nickname='Player5', clan_id=clan.id),
            Player.objects.create(nickname='Player6', clan_id=clan.id),
            Player.objects.create(nickname='Player7', clan_id=clan.id),
            ]
    return data


@pytest.fixture
def team():
    player1 = Player.objects.create(nickname='Player1')
    player2 = Player.objects.create(nickname='Player2')
    player3 = Player.objects.create(nickname='Player3')
    player4 = Player.objects.create(nickname='Player4')
    player5 = Player.objects.create(nickname='Player5')
    team = Team.objects.create(name='Team1')
    team.players.add(player1, player2, player3, player4, player5)
    return team


@pytest.fixture
def teams():
    data = [Team.objects.create(name='Team1'),
            Team.objects.create(name='Team2'),
            Team.objects.create(name='Team3'),
            Team.objects.create(name='Team4'),
            Team.objects.create(name='Team5'),
            Team.objects.create(name='Team6'),
            Team.objects.create(name='Team7'),
            ]
    return data


@pytest.fixture
def tank_type():
    return TankType.objects.create(name='TankType1')


@pytest.fixture
def tank_types():
    data = [TankType.objects.create(name='TankType1'),
            TankType.objects.create(name='TankType2'),
            TankType.objects.create(name='TankType3'),
            TankType.objects.create(name='TankType4'),
            TankType.objects.create(name='TankType5'),
            TankType.objects.create(name='TankType6'),
            TankType.objects.create(name='TankType7'),
            ]
    return data


@pytest.fixture
def nation():
    return Nation.objects.create(name='Nation1')


@pytest.fixture
def nations():
    data = [Nation.objects.create(name='Nation1'),
            Nation.objects.create(name='Nation2'),
            Nation.objects.create(name='Nation3'),
            Nation.objects.create(name='Nation4'),
            Nation.objects.create(name='Nation5'),
            Nation.objects.create(name='Nation6'),
            Nation.objects.create(name='Nation7'),
            ]
    return data


@pytest.fixture
def tank(nation, tank_type):
    return Tank.objects.create(name='Tank1', nation_id=nation.id, type_id=tank_type.id, tier=8)


@pytest.fixture
def tanks(nation, tank_type):
    data = [Tank.objects.create(name='Tank1', nation_id=nation.id, type_id=tank_type.id, tier=8),
            Tank.objects.create(name='Tank2', nation_id=nation.id, type_id=tank_type.id, tier=8),
            Tank.objects.create(name='Tank3', nation_id=nation.id, type_id=tank_type.id, tier=8),
            Tank.objects.create(name='Tank4', nation_id=nation.id, type_id=tank_type.id, tier=8),
            Tank.objects.create(name='Tank5', nation_id=nation.id, type_id=tank_type.id, tier=8),
            Tank.objects.create(name='Tank6', nation_id=nation.id, type_id=tank_type.id, tier=8),
            Tank.objects.create(name='Tank7', nation_id=nation.id, type_id=tank_type.id, tier=8),
            ]
    return data


@pytest.fixture
def player_tank(player, tank):
    return PlayerTank.objects.create(player_id=player.id, tank_id=tank.id)


@pytest.fixture
def player_tanks(player, tank):
    data = [PlayerTank.objects.create(player_id=player.id, tank_id=tank.id),
            PlayerTank.objects.create(player_id=player.id, tank_id=tank.id),
            PlayerTank.objects.create(player_id=player.id, tank_id=tank.id),
            PlayerTank.objects.create(player_id=player.id, tank_id=tank.id),
            PlayerTank.objects.create(player_id=player.id, tank_id=tank.id),
            PlayerTank.objects.create(player_id=player.id, tank_id=tank.id),
            PlayerTank.objects.create(player_id=player.id, tank_id=tank.id),
            ]
    return data


@pytest.fixture
def game(teams):
    return Game.objects.create(date_played=datetime.now(), team1_id=teams[0].id, team2_id=teams[1].id)


@pytest.fixture
def games(teams):
    data = [Game.objects.create(date_played=datetime.now(), team1_id=teams[0].id, team2_id=teams[1].id),
            Game.objects.create(date_played=datetime.now(), team1_id=teams[0].id, team2_id=teams[1].id),
            Game.objects.create(date_played=datetime.now(), team1_id=teams[0].id, team2_id=teams[1].id),
            Game.objects.create(date_played=datetime.now(), team1_id=teams[0].id, team2_id=teams[1].id),
            Game.objects.create(date_played=datetime.now(), team1_id=teams[0].id, team2_id=teams[1].id),
            Game.objects.create(date_played=datetime.now(), team1_id=teams[0].id, team2_id=teams[1].id),
            Game.objects.create(date_played=datetime.now(), team1_id=teams[0].id, team2_id=teams[1].id),
            ]
    return data


@pytest.fixture
def game_result(game, teams):
    return GameResult.objects.create(game_id=game.id, winner_team_id=teams[0].id)


@pytest.fixture
def game_results(teams):
    data = [GameResult.objects.create(game_id=Game.objects.create(date_played=datetime.now(),
                team1_id=teams[0].id, team2_id=teams[1].id).id, winner_team_id=teams[0].id),
            GameResult.objects.create(game_id=Game.objects.create(date_played=datetime.now(),
                team1_id=teams[0].id, team2_id=teams[1].id).id, winner_team_id=teams[0].id),
            GameResult.objects.create(game_id=Game.objects.create(date_played=datetime.now(),
                team1_id=teams[0].id, team2_id=teams[1].id).id, winner_team_id=teams[0].id),
            GameResult.objects.create(game_id=Game.objects.create(date_played=datetime.now(),
                team1_id=teams[0].id, team2_id=teams[1].id).id, winner_team_id=teams[0].id),
            GameResult.objects.create(game_id=Game.objects.create(date_played=datetime.now(),
                team1_id=teams[0].id, team2_id=teams[1].id).id, winner_team_id=teams[0].id),
            GameResult.objects.create(game_id=Game.objects.create(date_played=datetime.now(),
                team1_id=teams[0].id, team2_id=teams[1].id).id, winner_team_id=teams[0].id),
            GameResult.objects.create(game_id=Game.objects.create(date_played=datetime.now(),
                team1_id=teams[0].id, team2_id=teams[1].id).id, winner_team_id=teams[0].id),
            ]
    return data
