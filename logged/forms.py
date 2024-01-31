from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from players.models import *
from django.db.models import Q


class LoginForm(forms.Form):
    form_name = 'Login'
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class AddGamesForm(forms.Form):
    pass


class AddPlayersForm(forms.Form):
    form_name = 'Add New Player'
    nickname = forms.CharField(max_length=255)
    clan = forms.ModelChoiceField(queryset=Clan.objects.all(), required=False)


class AddTanksForm(forms.Form):
    form_name = 'Add New Tank'
    name = forms.CharField(max_length=255, required=True)
    tier = forms.IntegerField(min_value=1, max_value=10, required=True)
    nation = forms.ModelChoiceField(queryset=Nation.objects.all(), required=True)
    type = forms.ModelChoiceField(queryset=TankType.objects.all(), required=True)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Tank.objects.filter(name=name).exists():
            raise ValidationError('Tank with this name already exists')
        return name


def check_if_same_player_in_team(player1, player2, player3, player4, player5):
    players = [player1, player2, player3, player4, player5]
    if len(set(players)) < len(players):
        raise ValidationError("Players in the team must be unique.")


class AddTeamsForm(forms.Form):
    form_name = 'Add New Team'
    name = forms.CharField(max_length=255)
    player1 = forms.ModelChoiceField(queryset=Player.objects.all(), label='Player 1')
    player2 = forms.ModelChoiceField(queryset=Player.objects.all(), label='Player 2')
    player3 = forms.ModelChoiceField(queryset=Player.objects.all(), label='Player 3')
    player4 = forms.ModelChoiceField(queryset=Player.objects.all(), label='Player 4')
    player5 = forms.ModelChoiceField(queryset=Player.objects.all(), label='Player 5')

    team_name_duplicate_error = 'Team with this name already exists'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Team.objects.filter(name=name).exists():
            raise ValidationError(self.team_name_duplicate_error)
        return name

    def clean(self):
        cleaned_data = super().clean()
        player1 = cleaned_data.get('player1')
        player2 = cleaned_data.get('player2')
        player3 = cleaned_data.get('player3')
        player4 = cleaned_data.get('player4')
        player5 = cleaned_data.get('player5')

        check_if_same_player_in_team(player1, player2, player3, player4, player5)

        return cleaned_data
