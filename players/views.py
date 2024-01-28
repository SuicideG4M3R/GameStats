from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from players.models import *


class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')


class ListPlayersView(View):
    def get(self, request):
        players = Player.objects.all()
        return render(request, 'list_view.html', {'object_list': players})


class ListGamesView(View):
    def get(self, request):
        games = GameResult.objects.all()
        return render(request, 'list_view.html', {'object_list': games})


class ListClansView(View):
    def get(self, request):
        clans = Clan.objects.all()
        return render(request, 'list_view.html', {'object_list': clans})


class ListTanksView(View):
    def get(self, request):
        tanks = Tank.objects.all()
        return render(request, 'list_view.html', {'object_list': tanks})


class ListTeamsView(View):
    def get(self, request):
        teams = Team.objects.all()
        return render(request, 'list_view.html', {'object_list': teams})