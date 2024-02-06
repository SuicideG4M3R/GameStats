import random
from datetime import datetime
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from logged.forms import *


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', 'home')
                return redirect(next)
        return render(request, 'add_form.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('home')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if User.objects.all().count() == 0:
                user = User.objects.create_superuser(username=username, password=password)
                messages.success(request, f'Successfully created SUPER user: {username}')
            else:
                user = User.objects.create_user(username=username, password=password)
                messages.success(request, f'Successfully created user: {username}')

                ################################
                if not Group.objects.filter(name='New user').exists():
                    group = Group.objects.create(name='New user')
                    group.permissions.set(Permission.objects.all())  # NEW USER GROUP AND PERMISSIONS
                    user.groups.add(group)
                else:
                    group = Group.objects.get(name='New user')
                    user.groups.add(group)
                ################################

            login(request, user)
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})


class AddGamesView(PermissionRequiredMixin, View):
    permission_required = ['players.add_game']

    def get(self, request):
        form = AddGamesForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = AddGamesForm(request.POST)
        if form.is_valid():
            team1 = form.cleaned_data['team1']
            team2 = form.cleaned_data['team2']
            winner = int(form.cleaned_data['winner'])
            if winner == 1:
                winner = team1
            else:
                winner = team2
            game = Game.objects.create(team1=team1, team2=team2)
            GameResult.objects.create(winner_team=winner, game=game)
            messages.success(request,
                             f'Added game between team: {team1.name} vs team: {team2.name} --> Winner! {winner.name}')
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})


class AddPlayersView(PermissionRequiredMixin, View):
    permission_required = ['players.add_player']

    def get(self, request):
        form = AddPlayersForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = AddPlayersForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data.get('nickname')
            clan = form.cleaned_data.get('clan')
            Player.objects.create(nickname=nickname, clan=clan)
            messages.success(request, f'Added player: {nickname} to database')
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})


class AddClansView(PermissionRequiredMixin, View):
    permission_required = ['players.add_clan']

    def get(self, request):
        form = AddClanForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = AddClanForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            Clan.objects.create(name=name, description=description)
            messages.success(request, f'Successfully added {name}')
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})


class AddTanksView(PermissionRequiredMixin, View):
    permission_required = ['players.add_tank']

    def get(self, request):
        form = AddTanksForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = AddTanksForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            tier = form.cleaned_data.get('tier')
            nation = form.cleaned_data.get('nation')
            type = form.cleaned_data.get('type')
            Tank.objects.create(name=name, tier=tier, nation=nation, type=type)
            messages.success(request, f'Added tank: {name} to database')
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})


class AddTeamsView(PermissionRequiredMixin, View):
    permission_required = ['players.add_team']

    def get(self, request):
        form = AddTeamsForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = AddTeamsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            player1 = form.cleaned_data.get('player1')
            player2 = form.cleaned_data.get('player2')
            player3 = form.cleaned_data.get('player3')
            player4 = form.cleaned_data.get('player4')
            player5 = form.cleaned_data.get('player5')
            team = Team.objects.create(name=name)
            team.players.add(player1, player2, player3, player4, player5)
            team.save()
            messages.success(request, f'Added team: {name}: {player1} {player2} {player3} {player4} {player5}')
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})


class AddBasicDataView(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, f'Only admins can generate basic data')
        return redirect('home')

    def get(self, request, amount):
        counter = 1
        cycle = 0
        while amount > cycle:
            if Clan.objects.filter(name=f'Basic Clan {counter}').exists():
                counter += 1
            else:
                try:
                    clan = Clan.objects.create(name=f'Basic Clan {counter}',
                                               description=f'Description of Basic Clan {counter}')
                    player1 = Player.objects.create(nickname=f'Basic PlayerA {counter}', clan_id=clan.id)
                    player2 = Player.objects.create(nickname=f'Basic PlayerB {counter}', clan_id=clan.id)
                    player3 = Player.objects.create(nickname=f'Basic PlayerC {counter}', clan_id=clan.id)
                    player4 = Player.objects.create(nickname=f'Basic PlayerD {counter}', clan_id=clan.id)
                    player5 = Player.objects.create(nickname=f'Basic PlayerE {counter}', clan_id=clan.id)
                    player11 = Player.objects.create(nickname=f'Basic PlayerF {counter}', clan_id=clan.id)
                    player12 = Player.objects.create(nickname=f'Basic PlayerG {counter}', clan_id=clan.id)
                    player13 = Player.objects.create(nickname=f'Basic PlayerH {counter}', clan_id=clan.id)
                    player14 = Player.objects.create(nickname=f'Basic PlayerI {counter}', clan_id=clan.id)
                    player15 = Player.objects.create(nickname=f'Basic PlayerJ {counter}', clan_id=clan.id)
                    team1 = Team.objects.create(name=f'Basic TeamA {counter}')
                    team2 = Team.objects.create(name=f'Basic TeamB {counter}')
                    tank_type = TankType.objects.create(name=f'Basic Tank Type {counter}')
                    nation = Nation.objects.create(name=f'Basic Nation {counter}')
                    tank = Tank.objects.create(name=f'Basic Tank {counter}', nation_id=nation.id,
                                               type_id=tank_type.id, tier=random.randint(1, 10))

                    players = [player1, player2, player3, player4, player5, player11, player12, player13, player14,
                               player15]
                    for player in players:
                        PlayerTank.objects.create(player_id=player.id, tank_id=tank.id)

                    team1.players.add(player1, player2, player3, player4, player5)
                    team2.players.add(player11, player12, player13, player14, player15)

                    game = Game.objects.create(date_played=datetime.now(),
                                               team1_id=team1.id, team2_id=team2.id)
                    GameResult.objects.create(game_id=game.id, winner_team_id=team1.id)
                    cycle += 1
                    counter += 1
                    print(f'Successfully created data for cycle {cycle}')
                except Exception as error:
                    print(f'Error creating data for cycle {cycle}')
                    print(f'Error creating data for counter {counter}')
                    print(f'Error: {error}')
                    return HttpResponse(
                        f'Error: {error} has occurred when creating data for cycle: {cycle} with counter: {counter}')

        messages.success(request, f'Added basic data in amount of {amount} units.')
        return redirect('home')
