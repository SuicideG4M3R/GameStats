import pytest
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from logged.forms import *
from players.forms import *


# ##################################### LOGIN / LOGOUT #####################################

@pytest.mark.django_db
def test_home_logged(my_user):
    client = Client()
    client.force_login(my_user)
    url = reverse('home')
    response = client.get(url)
    assert 'Jarosław' in response.content.decode('utf-8')
    assert my_user.username in response.content.decode('utf-8')
    assert 'Add Players' in response.content.decode('utf-8')
    assert 'Add Clans' in response.content.decode('utf-8')
    assert 'Add Games' in response.content.decode('utf-8')
    assert 'Add Tanks' in response.content.decode('utf-8')
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_not_logged():
    client = Client()
    url = reverse('home')
    response = client.get(url)
    assert 'Jarosław' not in response.content.decode('utf-8')
    assert 'Add Players' not in response.content.decode('utf-8')
    assert 'Add Clans' not in response.content.decode('utf-8')
    assert 'Add Games' not in response.content.decode('utf-8')
    assert 'Add Tanks' not in response.content.decode('utf-8')
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_get():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], LoginForm)


@pytest.mark.django_db
def test_login_view_post(my_user):
    client = Client()
    url = reverse('login')
    data = {
        'username': my_user.username,
        'password': '12345678',
    }
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_view_get(my_user):
    client = Client()
    client.force_login(my_user)
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_view_get_not_logged():
    client = Client()
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302


# ##################################### Registry #####################################

@pytest.mark.django_db
def test_register_view_get():
    client = Client()
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], RegisterForm)


@pytest.mark.django_db
def test_register_view_post_first_superuser():
    client = Client()
    url = reverse('register')
    data = {
        'username': 'test',
        'password': 'testtest',
        'password2': 'testtest',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(username='test').exists()
    assert not Group.objects.filter(name='New user').exists()
    assert User.objects.get(username='test').is_authenticated
    assert User.objects.get(username='test').is_superuser


@pytest.mark.django_db
def test_register_view_post_second_register(my_user):
    client = Client()
    url = reverse('register')
    data = {
        'username': 'test2',
        'password': 'test2test2',
        'password2': 'test2test2',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Group.objects.filter(name='New user').exists()
    assert User.objects.filter(username='test2').exists()
    assert User.objects.get(username='test2').is_authenticated


# ##################################### LIST VIEWS #####################################


@pytest.mark.django_db
def test_list_games_single_view(game_result):
    client = Client()
    url = reverse('games_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 1


@pytest.mark.django_db
def test_list_games_view(game_results):
    client = Client()
    url = reverse('games_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 7
    for item in game_results:
        assert item in response.context['object_list']


@pytest.mark.django_db
def test_list_clans_single_view(clan):
    client = Client()
    url = reverse('clans_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 1


@pytest.mark.django_db
def test_list_clans_view(clans):
    client = Client()
    url = reverse('clans_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 7
    for item in clans:
        assert item in response.context['object_list']


@pytest.mark.django_db
def test_list_tanks_single_view(tank):
    client = Client()
    url = reverse('tanks_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 1


@pytest.mark.django_db
def test_list_tanks_view(tanks):
    client = Client()
    url = reverse('tanks_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 7
    for item in tanks:
        assert item in response.context['object_list']


@pytest.mark.django_db
def test_list_teams_single_view(team):
    client = Client()
    url = reverse('teams_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 1


@pytest.mark.django_db
def test_list_teams_view(teams):
    client = Client()
    url = reverse('teams_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 7
    for item in teams:
        assert item in response.context['object_list']


@pytest.mark.django_db
def test_list_players_single_view(player):
    client = Client()
    url = reverse('players_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 1


@pytest.mark.django_db
def test_list_players_view(players):
    client = Client()
    url = reverse('players_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['object_list'].count() == 7
    for item in players:
        assert item in response.context['object_list']


# ##################################### ADD VIEWS #####################################


@pytest.mark.django_db
def test_add_game_view_get_not_logged():
    client = Client()
    url = reverse('add_games')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_game_view_get_no_permissions(my_user):
    client = Client()
    client.force_login(my_user)
    url = reverse('add_games')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_game_view_get_with_permissions(my_user_with_permissions):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_games')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddGamesForm)


@pytest.mark.django_db
def test_add_game_view_post(my_user_with_permissions, teams):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_games')
    data = {
        'team1': teams[0].id,
        'team2': teams[1].id,
        'winner': 1
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Game.objects.all().count() == 1


@pytest.mark.django_db
def test_add_player_view_get_not_logged():
    client = Client()
    url = reverse('add_players')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_player_view_get_no_permissions(my_user):
    client = Client()
    client.force_login(my_user)
    url = reverse('add_players')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_player_view_get_with_permissions(my_user_with_permissions):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_players')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddPlayersForm)


@pytest.mark.django_db
def test_add_player_view_post(my_user_with_permissions, clan):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_players')
    nickname = 'TestPlayerName'
    data = {
        'nickname': nickname,
        'clan': clan.id
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Player.objects.all().count() == 1
    assert Player.objects.filter(nickname=nickname).exists()


@pytest.mark.django_db
def test_add_clan_view_get_not_logged():
    client = Client()
    url = reverse('add_clans')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_clan_view_get_no_permissions(my_user):
    client = Client()
    client.force_login(my_user)
    url = reverse('add_clans')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_clan_view_get_with_permissions(my_user_with_permissions):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_clans')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddClanForm)


@pytest.mark.django_db
def test_add_clan_view_post(my_user_with_permissions):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_clans')
    name = 'TestClanName'
    data = {
        'name': name,
        'description': 'TestClanDescription'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Clan.objects.all().count() == 1
    assert Clan.objects.filter(name=name).exists()


@pytest.mark.django_db
def test_add_tank_view_get_not_logged():
    client = Client()
    url = reverse('add_tanks')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_tank_view_get_no_permissions(my_user):
    client = Client()
    client.force_login(my_user)
    url = reverse('add_tanks')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_tank_view_get_with_permissions(my_user_with_permissions):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_tanks')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddTanksForm)


@pytest.mark.django_db
def test_add_tank_view_post(my_user_with_permissions, nation, tank_type):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_tanks')
    name = 'TestTankName'
    data = {
        'name': name,
        'tier': 10,
        'nation': nation.id,
        'type': tank_type.id
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Tank.objects.all().count() == 1
    assert Tank.objects.filter(name=name).exists()


@pytest.mark.django_db
def test_add_team_view_get_not_logged():
    client = Client()
    url = reverse('add_teams')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_team_view_get_no_permissions(my_user):
    client = Client()
    client.force_login(my_user)
    url = reverse('add_teams')
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_team_view_get_with_permissions(my_user_with_permissions):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_teams')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddTeamsForm)


@pytest.mark.django_db
def test_add_team_view_post(my_user_with_permissions, players):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_teams')
    name = 'TestTeamName'
    data = {
        'name': name,
        'player1': players[1].id,
        'player2': players[2].id,
        'player3': players[3].id,
        'player4': players[4].id,
        'player5': players[5].id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Team.objects.all().count() == 1
    assert Team.objects.filter(name=name).exists()


# ##################################### DETAIL VIEWS #####################################

# ##################################### SPECIAL SUPERUSER VIEWS #####################################

@pytest.mark.django_db
def test_special_not_user_basedata_generator_view():
    client = Client()
    amount = 10
    url = reverse('admin_base_data', kwargs={'amount': amount})
    response = client.get(url)
    assert response.status_code == 302
    assert not Clan.objects.all().count() == amount
    assert not Nation.objects.all().count() == amount
    assert not Tank.objects.all().count() == amount
    assert not Team.objects.all().count() == amount * 2
    assert not TankType.objects.all().count() == amount
    assert not Player.objects.all().count() == amount * 10
    assert not Game.objects.all().count() == amount
    assert not GameResult.objects.all().count() == amount


@pytest.mark.django_db
def test_special_user_with_permissions_basedata_generator_view(my_user_with_permissions):
    client = Client()
    client.force_login(my_user_with_permissions)
    amount = 10
    url = reverse('admin_base_data', kwargs={'amount': amount})
    response = client.get(url)
    assert response.status_code == 302
    assert not Clan.objects.all().count() == amount
    assert not Nation.objects.all().count() == amount
    assert not Tank.objects.all().count() == amount
    assert not Team.objects.all().count() == amount * 2
    assert not TankType.objects.all().count() == amount
    assert not Player.objects.all().count() == amount * 10
    assert not Game.objects.all().count() == amount
    assert not GameResult.objects.all().count() == amount


@pytest.mark.django_db
def test_special_superuser_basedata_generator_view(my_superuser):
    client = Client()
    client.force_login(my_superuser)
    amount = 10
    url = reverse('admin_base_data', kwargs={'amount': amount})
    response = client.get(url)
    assert response.status_code == 302
    assert Clan.objects.all().count() == amount
    assert Nation.objects.all().count() == amount
    assert Tank.objects.all().count() == amount
    assert Team.objects.all().count() == amount * 2
    assert TankType.objects.all().count() == amount
    assert Player.objects.all().count() == amount * 10
    assert Game.objects.all().count() == amount
    assert GameResult.objects.all().count() == amount
