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
from players import views

urlpatterns = [
    path('players/', views.ListPlayersView.as_view(), name='players_list'),
    path('games/', views.ListGamesView.as_view(), name='games_list'),
    path('clans/', views.ListClansView.as_view(), name='clans_list'),
    path('tanks/', views.ListTanksView.as_view(), name='tanks_list'),
    path('teams/', views.ListTeamsView.as_view(), name='teams_list'),
]
