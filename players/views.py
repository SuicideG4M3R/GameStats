from django.http import HttpResponse
from django.shortcuts import render
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