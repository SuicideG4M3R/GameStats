import pytest
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from logged.forms import LoginForm


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


