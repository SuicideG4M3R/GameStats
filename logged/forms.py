from django import forms
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.forms import Select

from players.models import *
from django.db.models import Q


class LoginForm(forms.Form):
    form_name = 'Login'
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    form_name = 'Register'
    password = forms.CharField(max_length=50, min_length=8,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')

    password2 = forms.CharField(max_length=50, min_length=8,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Re-Password')

    class Meta:
        model = User
        fields = ['username',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password is None or password2 is None or password != password2:
            raise ValidationError('Passwords do not match.')
        if len(password) < 8 or 8 > len(password2):
            raise ValidationError('Password must be at least 8 characters long.')
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username


class AddGamesForm(forms.Form):
    form_name = 'Add New Game'
    teams = Team.objects.all()
    team1 = forms.ModelChoiceField(queryset=teams, required=True, label='Team 1')
    team2 = forms.ModelChoiceField(queryset=teams, required=True, label='Team 2')
    winner = forms.ChoiceField(choices=[(1, 'Team 1'), (2, 'Team 2')], required=True, label='Won')

    def clean(self):
        cleaned_data = super().clean()
        team1 = cleaned_data.get('team1')
        team2 = cleaned_data.get('team2')
        if team1 == team2:
            raise ValidationError('Teams cannot be the same.')
        return cleaned_data


class AddPlayersForm(forms.Form):
    form_name = 'Add New Player'
    nickname = forms.CharField(max_length=255)
    clan = forms.ModelChoiceField(queryset=Clan.objects.all(), required=False)

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if Player.objects.filter(nickname=nickname).exists():
            raise ValidationError('Player with this nickname already exists')
        return nickname


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

    def clean_tier(self):
        tier = self.cleaned_data.get('tier')
        if tier > 10 or tier < 1:
            raise ValidationError('Tier must be between 1 and 10')
        return tier


def check_if_same_player_in_team(player1, player2, player3, player4, player5):
    players = [player1, player2, player3, player4, player5]
    if len(set(players)) < len(players):
        raise ValidationError("Players in the team must be unique.")


class AddTeamsForm(forms.Form):
    form_name = 'Add New Team'
    name = forms.CharField(max_length=255)
    players = Player.objects.all()
    player1 = forms.ModelChoiceField(queryset=players, label='Player 1')
    player2 = forms.ModelChoiceField(queryset=players, label='Player 2')
    player3 = forms.ModelChoiceField(queryset=players, label='Player 3')
    player4 = forms.ModelChoiceField(queryset=players, label='Player 4')
    player5 = forms.ModelChoiceField(queryset=players, label='Player 5')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Team.objects.filter(name=name).exists():
            raise ValidationError('Team with this name already exists')
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


class AddClanForm(forms.Form):
    form_name = 'Add New Clan'
    name = forms.CharField(max_length=50, min_length=3, required=True)
    description = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'cols': 40, 'rows': 4}))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise ValidationError('Clan name must be at least 3 characters long')
        if Clan.objects.filter(name=name).exists():
            raise ValidationError('Clan with this name already exists')
        return name
