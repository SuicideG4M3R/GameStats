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
    path('player/<int:id>/add-tank/', views.AddTankToPlayerView.as_view(), name='add_tank_to_player'),
    path('player/<int:id>/delete-tank/', views.DeleteTankFromPlayerView.as_view(), name='delete_tank_to_player'),
    path('addClans/', views.AddClansView.as_view(), name='add_clans'),
    path('addTanks/', views.AddTanksView.as_view(), name='add_tanks'),
    path('addTeams/', views.AddTeamsView.as_view(), name='add_teams'),

    path('game/<int:id>/edit/', views.EditGameView.as_view(), name='edit_game'),
    path('player/<int:id>/edit/', views.EditPlayerView.as_view(), name='edit_player'),
    path('clan/<int:id>/edit/', views.EditClanView.as_view(), name='edit_clan'),
    path('tank/<int:id>/edit/', views.EditTankView.as_view(), name='edit_tank'),
    path('team/<int:id>/edit/', views.EditTeamView.as_view(), name='edit_team'),

    path('game/<int:id>/delete/', views.DeleteGameView.as_view(), name='delete_game'),
    path('player/<int:id>/delete/', views.DeletePlayerView.as_view(), name='delete_player'),
    path('clan/<int:id>/delete/', views.DeleteClanView.as_view(), name='delete_clan'),
    path('tank/<int:id>/delete/', views.DeleteTankView.as_view(), name='delete_tank'),
    path('team/<int:id>/delete/', views.DeleteTeamView.as_view(), name='delete_team'),

    path('addBasicData/<int:amount>/', views.AddBasicDataView.as_view(), name='admin_base_data'),
    # ADDS BASIC DATA PRE-GENERATED

]
