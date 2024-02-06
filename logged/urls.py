"""
URL configuration for GameStats project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from logged import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('addGames/', views.AddGamesView.as_view(), name='add_games'),
    path('addPlayers/', views.AddPlayersView.as_view(), name='add_players'),
    path('addClans/', views.AddClansView.as_view(), name='add_clans'),
    path('addTanks/', views.AddTanksView.as_view(), name='add_tanks'),
    path('addTeams/', views.AddTeamsView.as_view(), name='add_teams'),
    path('game/<int:id>/', views.GameDetailView.as_view(), name='game_detail'),
    path('player/<int:id>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('clan/<int:id>/', views.ClanDetailView.as_view(), name='clan_detail'),
    path('tank/<int:id>/', views.TankDetailView.as_view(), name='tank_detail'),
    path('team/<int:id>/', views.TeamDetailView.as_view(), name='team_detail'),

    path('addBasicData/<int:amount>/', views.AddBasicDataView.as_view(), name='admin_base_data'),  # ADDS BASIC DATA PRE-GENERATED

]
