import pytest
from django.test import Client
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


@pytest.mark.django_db
def test_add_tank_to_player_view_get_with_permissions(my_user_with_permissions, player):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_tank_to_player', args=(player.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddTankToPlayerForm)


@pytest.mark.django_db
def test_add_tank_to_player_view_post(my_user_with_permissions, player, tank):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('add_tank_to_player', args=(player.id,))
    data = {
        'tank': tank.id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert player.tanks.filter(id=tank.id).exists()


@pytest.mark.django_db
def test_delete_tank_from_player_view_get_with_permissions(my_user_with_permissions, player):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('delete_tank_to_player', args=(player.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], DeleteTankFromPlayerForm)


@pytest.mark.django_db
def test_delete_tank_from_player_view_post(my_user_with_permissions, player, tank):
    client = Client()
    client.force_login(my_user_with_permissions)
    player.tanks.add(tank)
    url = reverse('delete_tank_to_player', args=(player.id,))
    data = {
        'tank': tank.id,
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert not player.tanks.filter(id=tank.id).exists()

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

@pytest.mark.django_db
def test_game_detail_view_get(game_result):
    client = Client()
    url = reverse('game_detail', args=(game_result.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'context' in response.context
    assert game_result.winner_team in response.context['context'].values()
    assert game_result.id in response.context['context'].values()


@pytest.mark.django_db
def test_game_detail_view_get_non_existing():
    client = Client()
    url = reverse('game_detail', args=(1,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_player_detail_view_get(player):
    client = Client()
    url = reverse('player_detail', args=(player.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'context' in response.context
    assert player.nickname in response.context['context'].values()
    assert player.clan in response.context['context'].values()


@pytest.mark.django_db
def test_player_detail_view_get_non_existing():
    client = Client()
    url = reverse('player_detail', args=(1,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_tank_detail_view_get(tank):
    client = Client()
    url = reverse('tank_detail', args=(tank.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'context' in response.context
    assert tank.name in response.context['context'].values()
    assert tank.tier in response.context['context'].values()
    assert tank.type in response.context['context'].values()
    assert tank.nation in response.context['context'].values()


@pytest.mark.django_db
def test_tank_detail_view_get_non_existing():
    client = Client()
    url = reverse('tank_detail', args=(1,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_clan_detail_view_get(clan):
    client = Client()
    url = reverse('clan_detail', args=(clan.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'context' in response.context
    assert clan.name in response.context['context'].values()
    assert clan.description in response.context['context'].values()


@pytest.mark.django_db
def test_clan_detail_view_get_non_existing():
    client = Client()
    url = reverse('clan_detail', args=(1,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_team_detail_view_get(team):
    client = Client()
    url = reverse('team_detail', args=(team.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert team.name in response.context['context'].values()
    assert team.id in response.context['context'].values()


@pytest.mark.django_db
def test_team_detail_view_get_non_existing():
    client = Client()
    url = reverse('team_detail', args=(1,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('home')


# ##################################### EDIT VIEWS #####################################

@pytest.mark.django_db
def test_game_edit_view_get(my_superuser, game_result):
    client = Client()
    client.force_login(my_superuser)
    url = reverse('edit_game', args=(game_result.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddGamesForm)


@pytest.mark.django_db
def test_game_edit_view_post(my_superuser, game_result):
    client = Client()
    client.force_login(my_superuser)
    url = reverse('edit_game', args=(game_result.id,))
    before = game_result.winner_team_id
    data = {
        'team1': game_result.game.team1_id,
        'team2': game_result.game.team2_id,
        'winner': 2
    }
    assert before != game_result.game.team2_id
    response = client.post(url, data)
    assert response.status_code == 302
    updated = GameResult.objects.get(id=game_result.id)
    assert updated.winner_team_id != str(before)
    assert updated.winner_team_id == game_result.game.team2_id


@pytest.mark.django_db
def test_player_edit_view_get(my_user_with_permissions, player):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('edit_player', args=(player.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddPlayersForm)


@pytest.mark.django_db
def test_player_edit_view_post(my_user_with_permissions, player):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('edit_player', args=(player.id,))
    form_data = {
        'nickname': 'Updated Nickname',
        'clan': player.clan_id
    }
    assert not player.nickname == 'Updated Nickname'
    response = client.post(url, form_data)
    assert response.status_code == 302
    player = Player.objects.get(id=player.id)
    assert player.nickname == 'Updated Nickname'


@pytest.mark.django_db
def test_tank_edit_view_get(my_user_with_permissions, tank):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('edit_tank', args=(tank.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddTanksForm)


@pytest.mark.django_db
def test_tank_edit_view_post(my_user_with_permissions, tank):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('edit_tank', args=(tank.id,))
    form_data = {
        'name': 'Updated Tank Name',
        'tier': 9,
        'nation': tank.nation_id,
        'type': tank.type_id
    }
    assert not tank.name == 'Updated Tank Name'
    assert tank.tier == 8
    response = client.post(url, form_data)
    assert response.status_code == 302
    tank = Tank.objects.get(id=tank.id)
    assert tank.name == 'Updated Tank Name'
    assert tank.tier == 9


@pytest.mark.django_db
def test_clan_edit_view_get(my_user_with_permissions, clan):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('edit_clan', args=(clan.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddClanForm)


@pytest.mark.django_db
def test_clan_edit_view_post(my_user_with_permissions, clan):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('edit_clan', args=(clan.id,))
    form_data = {
        'name': 'Updated Clan Name',
        'description': 'Updated description'
    }
    assert not clan.name == 'Updated Clan Name'
    assert not clan.description == 'Updated description'
    response = client.post(url, form_data)
    assert response.status_code == 302
    clan = Clan.objects.get(id=clan.id)
    assert clan.name == 'Updated Clan Name'
    assert clan.description == 'Updated description'


@pytest.mark.django_db
def test_team_edit_view_get(my_user_with_permissions, team):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('edit_team', args=(team.id,))
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert isinstance(response.context['form'], AddTeamsForm)


@pytest.mark.django_db
def test_team_edit_view_post(my_user_with_permissions, team):
    client = Client()
    client.force_login(my_user_with_permissions)
    url = reverse('edit_team', args=(team.id,))
    form_data = {
        'name': 'Updated Team Name',
        'player1': team.players.all()[0].id,
        'player2': team.players.all()[1].id,
        'player3': team.players.all()[2].id,
        'player4': team.players.all()[3].id,
        'player5': team.players.all()[4].id
    }
    assert not team.name == 'Updated Team Name'
    response = client.post(url, form_data)
    assert response.status_code == 302
    team = Team.objects.get(id=team.id)
    assert team.name == 'Updated Team Name'


# ##################################### DELETE SUPERUSER VIEWS #####################################

@pytest.mark.django_db
def test_games_delete_view_with_superuser_permissions(my_superuser, games):
    client = Client()
    client.force_login(my_superuser)
    assert Game.objects.all().count() == 7
    url = reverse('delete_game', args=(games[0].id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('games_list')
    assert Game.objects.all().count() == 6


@pytest.mark.django_db
def test_game_delete_view_with_no_permissions(my_user, games):
    client = Client()
    client.force_login(my_user)
    assert Game.objects.all().count() == 7
    url = reverse('delete_game', args=(games[0].id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('games_list')
    assert not Game.objects.all().count() == 6


@pytest.mark.django_db
def test_players_delete_view_with_permissions(my_user_with_permissions, players):
    client = Client()
    client.force_login(my_user_with_permissions)
    assert Player.objects.all().count() == 7
    url = reverse('delete_player', args=(players[0].id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('players_list')
    assert Player.objects.all().count() == 6


@pytest.mark.django_db
def test_player_delete_view_with_no_permissions(my_user, players):
    client = Client()
    client.force_login(my_user)
    assert Player.objects.all().count() == 7
    url = reverse('delete_player', args=(players[0].id,))
    response = client.get(url)
    assert response.status_code == 403
    assert not Player.objects.all().count() == 6


@pytest.mark.django_db
def test_tank_delete_view_with_permissions(my_user_with_permissions, tanks):
    client = Client()
    client.force_login(my_user_with_permissions)
    assert Tank.objects.all().count() == 7
    url = reverse('delete_tank', args=(tanks[0].id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('tanks_list')
    assert Tank.objects.all().count() == 6


@pytest.mark.django_db
def test_tank_delete_view_with_no_permissions(my_user, tanks):
    client = Client()
    client.force_login(my_user)
    assert Tank.objects.all().count() == 7
    url = reverse('delete_tank', args=(tanks[0].id,))
    response = client.get(url)
    assert response.status_code == 403
    assert not Tank.objects.all().count() == 6


@pytest.mark.django_db
def test_clan_delete_view_with_permissions(my_user_with_permissions, clans):
    client = Client()
    client.force_login(my_user_with_permissions)
    assert Clan.objects.all().count() == 7
    url = reverse('delete_clan', args=(clans[0].id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('clans_list')
    assert Clan.objects.all().count() == 6


@pytest.mark.django_db
def test_clan_delete_view_with_no_permissions(my_user, clans):
    client = Client()
    client.force_login(my_user)
    assert Clan.objects.all().count() == 7
    url = reverse('delete_clan', args=(clans[0].id,))
    response = client.get(url)
    assert response.status_code == 403
    assert not Clan.objects.all().count() == 6


@pytest.mark.django_db
def test_team_delete_view_with_permissions(my_user_with_permissions, teams):
    client = Client()
    client.force_login(my_user_with_permissions)
    assert Team.objects.all().count() == 7
    url = reverse('delete_team', args=(teams[0].id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('teams_list')
    assert Team.objects.all().count() == 6


@pytest.mark.django_db
def test_team_delete_view_with_no_permissions(my_user, teams):
    client = Client()
    client.force_login(my_user)
    assert Team.objects.all().count() == 7
    url = reverse('delete_team', args=(teams[0].id,))
    response = client.get(url)
    assert response.status_code == 403
    assert not Team.objects.all().count() == 6


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
