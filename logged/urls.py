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
    # path('addGames/', views.AddGamesView.as_view(), name='add_games'),
    path('addPlayers/', views.AddPlayersView.as_view(), name='add_players'),
    path('addClans/', views.AddClansView.as_view(), name='add_clans'),
    path('addTanks/', views.AddTanksView.as_view(), name='add_tanks'),
    path('addTeams/', views.AddTeamsView.as_view(), name='add_teams'),
]
