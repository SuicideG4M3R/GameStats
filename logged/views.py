from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
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
        return redirect('home')


# class AddGamesView(View):
#     def get(self, request):
#         form = AddGamesForm()
#         return render(request, 'add_form.html', {'form': form})


class AddPlayersView(View):
    def get(self, request):
        form = AddPlayersForm()
        return render(request, 'add_form.html', {'form': form})


class AddClansView(View):
    pass


class AddTanksView(View):
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
            messages.success(request, f'Added tank: {name} to database')
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})


class AddTeamsView(View):
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
            return redirect('home')
        return render(request, 'add_form.html', {'form': form})
