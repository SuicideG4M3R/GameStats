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
            return redirect('games_list')
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
            return redirect('players_list')
        return render(request, 'add_form.html', {'form': form})


class AddTankToPlayerView(PermissionRequiredMixin, View):
    permission_required = ['players.add_tank']

    def get(self, request, id):
        player = get_object_or_404(Player, id=id)
        form = AddTankToPlayerForm()

        return render(request, 'add_form.html', {'player': player, 'form': form})

    def post(self, request, id):
        player = get_object_or_404(Player, id=id)
        form = AddTankToPlayerForm(request.POST)
        if form.is_valid():
            tank_id = form.cleaned_data['tank'].id
            tank = get_object_or_404(Tank, id=tank_id)
            if player.tanks.filter(id=tank.id).exists():
                form.add_error(None, f'Tank {tank.name} already added to player {player.nickname}')
                return render(request, 'add_form.html', {'player': player, 'form': form})
            player.tanks.add(tank)
            messages.success(request, f'Tank {tank.name} added to player {player.nickname}')
            return redirect('player_detail', id=id)
        else:
            return render(request, 'add_form.html', {'player': player, 'form': form})


class DeleteTankFromPlayerView(PermissionRequiredMixin, View):
    permission_required = ['players.delete_tank']

    def get(self, request, id):
        player = get_object_or_404(Player, id=id)
        form = DeleteTankFromPlayerForm()
        return render(request, 'add_form.html', {'player': player, 'form': form})

    def post(self, request, id):
        player = get_object_or_404(Player, id=id)
        form = DeleteTankFromPlayerForm(request.POST)
        if form.is_valid():
            tank_id = form.cleaned_data['tank'].id
            tank = get_object_or_404(Tank, id=tank_id)
            if player.tanks.filter(id=tank.id).exists():
                player.tanks.remove(tank)
                messages.success(request, f'Tank {tank.name} removed from player {player.nickname}')
            else:
                form.add_error(None, f'{player.nickname} does not have {tank.name}')
                return render(request, 'add_form.html', {'player': player, 'form': form})
            return redirect('player_detail', id=id)
        else:
            return render(request, 'add_form.html', {'player': player, 'form': form})


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
            return redirect('clans_list')
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
            return redirect('tanks_list')
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
            return redirect('teams_list')
        return render(request, 'add_form.html', {'form': form})


class EditGameView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, f'Sorry, Only admins can edit game results')
        return redirect('games_list')

    def get_context_data(self, game):
        game_result = get_object_or_404(GameResult, id=game.id)
        context = {
            'Game id': game.id,
            'Played': game.date_played,
            'Team 1': game.team1,
            'Team 2': game.team2,
            'Winner': game_result.winner_team
        }
        return context

    def get(self, request, id):
        if Game.objects.filter(id=id).exists():
            game = Game.objects.get(id=id)
            game_result = GameResult.objects.get(id=id)
            form = AddGamesForm(initial={
                'team1': game.team1,
                'team2': game.team2,
                'winner': game_result.winner_team.id
            })
            context = self.get_context_data(game)
            return render(request, 'edit_form.html', {'form': form, 'context': context})
        else:
            messages.error(request, f'Game not found')
            return redirect('games_list')

    def post(self, request, id):
        form = AddGamesForm(request.POST)
        game = get_object_or_404(Game, id=id)
        if form.is_valid():
            team1 = form.cleaned_data['team1']
            team2 = form.cleaned_data['team2']
            winner = int(form.cleaned_data['winner'])
            if winner == 1:
                winner = team1
            else:
                winner = team2
            game.team1 = team1
            game.team2 = team2
            game.save()
            game_result = GameResult.objects.get(game=game)
            game_result.winner_team = winner
            game_result.save()
            messages.success(request,
                             f'Game details updated successfully')
            return redirect('games_list')
        else:
            context = self.get_context_data(game)
            return render(request, 'edit_form.html', {'form': form, 'context': context})


class EditPlayerView(PermissionRequiredMixin, View):
    permission_required = ['players.change_player']

    def get_context_data(self, player):
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
        return context

    def get(self, request, id):
        if Player.objects.filter(id=id).exists():
            player = Player.objects.get(id=id)
            form = AddPlayersForm(initial={
                'nickname': player.nickname,
                'clan': player.clan,
            })
            context = self.get_context_data(player)
            return render(request, 'edit_form.html', {'form': form, 'context': context})
        else:
            messages.error(request, f'Player with ID: {id} does not exist')
            return redirect('home')

    def post(self, request, id):
        form = AddPlayersForm(request.POST, is_edit=True)
        player = get_object_or_404(Player, id=id)
        context = self.get_context_data(player)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            clan = form.cleaned_data['clan']
            player.nickname = nickname
            player.clan = clan
            try:
                player.save()
            except IntegrityError:
                form.add_error(None, 'User with that nickname already exists')
                return render(request, 'edit_form.html', {'form': form, 'context': context})
            messages.success(request,
                             f'Player details updated successfully')
            return redirect('players_list')
        else:
            return render(request, 'edit_form.html', {'form': form, 'context': context})


class EditClanView(PermissionRequiredMixin, View):
    permission_required = ['players.change_clan']

    def get_context_data(self, clan):
        if Clan.objects.filter(id=clan.id).exists():
            context = {
                'Clan ID': clan.id,
                'Name': clan.name,
                'Description': clan.description
            }
            return context

    def get(self, request, id):
        if Clan.objects.filter(id=id).exists():
            clan = Clan.objects.get(id=id)
            form = AddClanForm(initial={
                'name': clan.name,
                'description': clan.description
            })
            context = self.get_context_data(clan)
            return render(request, 'edit_form.html', {'form': form, 'context': context})
        else:
            messages.error(request, f'Clan with ID: {id} does not exist')
            return redirect('clans_list')

    def post(self, request, id):
        form = AddClanForm(request.POST, is_edit=True)
        clan = get_object_or_404(Clan, id=id)
        context = self.get_context_data(clan)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            clan.name = name
            clan.description = description
            try:
                clan.save()
            except IntegrityError:
                form.add_error(None, 'Clan with that name already exists')
                return render(request, 'edit_form.html', {'form': form, 'context': context})
            messages.success(request,
                             f'Clan details updated successfully')
            return redirect('clans_list')
        else:
            return render(request, 'edit_form.html', {'form': form, 'context': context})


class EditTankView(PermissionRequiredMixin, View):
    permission_required = ['players.change_tank']

    def get_context_data(self, tank):
        if Tank.objects.filter(id=tank.id).exists():
            context = {
                'Tank ID': tank.id,
                'Name': tank.name,
                'Tier': tank.tier,
                'Nation': tank.nation,
                'Type': tank.type
            }
            return context

    def get(self, request, id):
        if Tank.objects.filter(id=id).exists():
            tank = Tank.objects.get(id=id)
            form = AddTanksForm(initial={
                'name': tank.name,
                'tier': tank.tier,
                'nation': tank.nation,
                'type': tank.type
            })
            context = self.get_context_data(tank)
            return render(request, 'edit_form.html', {'form': form, 'context': context})
        else:
            messages.error(request, f'Tank with ID: {id} does not exist')
            return redirect('tanks_list')

    def post(self, request, id):
        form = AddTanksForm(request.POST, is_edit=True)
        tank = get_object_or_404(Tank, id=id)
        context = self.get_context_data(tank)
        if form.is_valid():
            name = form.cleaned_data['name']
            tier = form.cleaned_data['tier']
            nation = form.cleaned_data['nation']
            type = form.cleaned_data['type']
            tank.name = name
            tank.tier = tier
            tank.nation = nation
            tank.type = type
            try:
                tank.save()
            except IntegrityError:
                form.add_error(None, 'Tank with that name already exists')
                return render(request, 'edit_form.html', {'form': form, 'context': context})
            messages.success(request,
                             f'Tank details updated successfully')
            return redirect('tanks_list')
        else:
            return render(request, 'edit_form.html', {'form': form, 'context': context})


class EditTeamView(PermissionRequiredMixin, View):
    permission_required = ['players.change_team']

    def get_context_data(self, team):
        if Team.objects.filter(id=team.id).exists():
            players = []
            for player in team.players.all().order_by('nickname'):
                players.append(player.nickname)
            context = {
                'Team ID': team.id,
                'Name': team.name,
                'Players': players
            }
            return context

    def get(self, request, id):
        if Team.objects.filter(id=id).exists():
            team = Team.objects.get(id=id)
            players = team.players.all().order_by('nickname')
            form = AddTeamsForm(initial={
                'name': team.name,
                'player1': players[0],
                'player2': players[1],
                'player3': players[2],
                'player4': players[3],
                'player5': players[4],
            })
            context = self.get_context_data(team)
            return render(request, 'edit_form.html', {'form': form, 'context': context})
        else:
            messages.error(request, f'Team with ID: {id} does not exist')
            return redirect('teams_list')

    def post(self, request, id):
        form = AddTeamsForm(request.POST, is_edit=True)
        team = get_object_or_404(Team, id=id)
        context = self.get_context_data(team)
        if form.is_valid():
            name = form.cleaned_data['name']
            player1 = form.cleaned_data['player1']
            player2 = form.cleaned_data['player2']
            player3 = form.cleaned_data['player3']
            player4 = form.cleaned_data['player4']
            player5 = form.cleaned_data['player5']
            team.name = name
            team.players.clear()
            team.players.add(player1, player2, player3, player4, player5)
            try:
                team.save()
            except IntegrityError:
                form.add_error(None, 'Team with that name already exists')
                return render(request, 'edit_form.html', {'form': form, 'context': context})
            messages.success(request,
                             f'Team details updated successfully')
            return redirect('teams_list')
        else:
            return render(request, 'edit_form.html', {'form': form, 'context': context})


class DeleteGameView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, f'Sorry, Only admins can delete game results')
        return redirect('games_list')

    def get(self, request, id):
        if Game.objects.filter(id=id).exists():
            Game.objects.get(id=id).delete()
            messages.success(request, f'Game with ID: {id} deleted successfully')
            return redirect('games_list')
        else:
            messages.error(request, f'Game with ID: {id} does not exist or has been already deleted before')
            return redirect('games_list')


class DeletePlayerView(PermissionRequiredMixin, View):
    permission_required = ['players.delete_player']

    def get(self, request, id):
        if Player.objects.filter(id=id).exists():
            player = Player.objects.get(id=id)
            if Team.objects.filter(players=player).exists():
                player_teams = Team.objects.filter(players=player)
                for team in player_teams:
                    team.delete()
            player.delete()
            messages.success(request, f'Player with ID: {id} deleted successfully')
            return redirect('players_list')
        else:
            messages.error(request, f'Player with ID: {id} does not exist or has been already deleted before')
            return redirect('players_list')


class DeleteClanView(PermissionRequiredMixin, View):
    permission_required = ['players.delete_clan']

    def get(self, request, id):
        if Clan.objects.filter(id=id).exists():
            Clan.objects.get(id=id).delete()
            messages.success(request, f'Clan with ID: {id} deleted successfully')
            return redirect('clans_list')
        else:
            messages.error(request, f'Clan with ID: {id} does not exist or has been already deleted before')
            return redirect('clans_list')


class DeleteTankView(PermissionRequiredMixin, View):
    permission_required = ['players.delete_tank']

    def get(self, request, id):
        if Tank.objects.filter(id=id).exists():
            Tank.objects.get(id=id).delete()
            messages.success(request, f'Tank with ID: {id} deleted successfully')
            return redirect('tanks_list')
        else:
            messages.error(request, f'Tank with ID: {id} does not exist or has been already deleted before')
            return redirect('tanks_list')


class DeleteTeamView(PermissionRequiredMixin, View):
    permission_required = ['players.delete_team']

    def get(self, request, id):
        if Team.objects.filter(id=id).exists():
            Team.objects.get(id=id).delete()
            messages.success(request, f'Team with ID: {id} deleted successfully')
            return redirect('teams_list')
        else:
            messages.error(request, f'Team with ID: {id} does not exist or has been already deleted before')
            return redirect('teams_list')


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
