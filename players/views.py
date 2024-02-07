from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from players.forms import *
from players.models import *


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class ListPlayersView(View):
    def get(self, request):
        players = Player.objects.all()
        form = PlayerSearchForm(request.GET)
        if form.is_valid():
            nickname = form.cleaned_data.get('nickname', '')
            players = players.filter(nickname__icontains=nickname)
        return render(request, 'list_view.html', {'object_list': players, 'form': form})


class ListGamesView(View):
    def get(self, request):
        games = GameResult.objects.all()
        form = GameResultSearchForm(request.GET)
        if form.is_valid():
            date_played = form.cleaned_data.get('date_played', '')
            if date_played:
                games = games.filter(game__date_played__icontains=date_played)
        return render(request, 'list_view.html', {'object_list': games, 'form': form})


class ListClansView(View):
    def get(self, request):
        clans = Clan.objects.all()
        form = ClanSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            clans = clans.filter(name__icontains=name)
        return render(request, 'list_view.html', {'object_list': clans, 'form': form})


class ListTanksView(View):
    def get(self, request):
        tanks = Tank.objects.all()
        form = TankSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            tanks = tanks.filter(name__icontains=name)
        return render(request, 'list_view.html', {'object_list': tanks, 'form': form})


class ListTeamsView(View):
    def get(self, request):
        teams = Team.objects.all()
        form = TeamSearchForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            teams = teams.filter(name__icontains=name)
        return render(request, 'list_view.html', {'object_list': teams, 'form': form})


class GameDetailView(View):
    def get(self, request, id):
        if Game.objects.filter(id=id).exists():
            game = get_object_or_404(Game, id=id)
            game_result = get_object_or_404(GameResult, id=game.id)
            context = {
                'Game id': game.id,
                'Played': game.date_played,
                'Team 1': game.team1,
                'Team 2': game.team2,
                'Winner': game_result.winner_team
            }
            return render(request, 'detail_view.html', {'context': context})
        else:
            messages.error(request, f'Game with ID: {id} does not exist')
            return redirect('home')


class PlayerDetailView(View):
    def get(self, request, id):
        if Player.objects.filter(id=id).exists():
            player = get_object_or_404(Player, id=id)
            if PlayerTank.objects.filter(player=player).count() == 0:
                tanks = 'None'
            else:
                tanks = []
                for tank in PlayerTank.objects.filter(player=player):
                    name = f'Tank {tank.tank.name}'
                    tanks.append(name)
            if Team.objects.filter(players=player).count() == 0:
                team_list = 'None'
            else:
                team_list = []
                for team in Team.objects.filter(players=player):
                    name = f'Team {team.name}'
                    team_list.append(name)

            context = {
                'Player ID': player.id,
                'Nickname': player.nickname,
                'Clan': player.clan,
                'Teams': team_list,
                'Tanks': tanks,
            }
            return render(request, 'detail_view.html', {'context': context, 'id': id})
        else:
            messages.error(request, f'Player with ID: {id} does not exist')
            return redirect('home')


class ClanDetailView(View):
    def get(self, request, id):
        if Clan.objects.filter(id=id).exists():
            clan = get_object_or_404(Clan, id=id)
            context = {
                'Clan ID': clan.id,
                'Name': clan.name,
                'Description': clan.description
            }
            return render(request, 'detail_view.html', {'context': context})
        else:
            messages.error(request, f'Clan with ID: {id} does not exist')
            return redirect('home')


class TankDetailView(View):
    def get(self, request, id):
        if Tank.objects.filter(id=id).exists():
            tank = get_object_or_404(Tank, id=id)
            context = {
                'Tank ID': tank.id,
                'Name': tank.name,
                'Tier': tank.tier,
                'Nation': tank.nation,
                'Type': tank.type
            }
            return render(request, 'detail_view.html', {'context': context})
        else:
            messages.error(request, f'Tank with ID: {id} does not exist')
            return redirect('home')


class TeamDetailView(View):
    def get(self, request, id):
        if Team.objects.filter(id=id).exists():
            team = get_object_or_404(Team, id=id)
            players = []
            for player in team.players.all():
                players.append(player.nickname)
            context = {
                'Team ID': team.id,
                'Name': team.name,
                'Players': players
            }
            return render(request, 'detail_view.html', {'context': context})
        else:
            messages.error(request, f'Team with ID: {id} does not exist')
            return redirect('home')
