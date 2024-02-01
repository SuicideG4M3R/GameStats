from django import forms
from django.forms import SelectDateWidget

from players.models import *


class ClanSearchForm(forms.Form):
    form_name = 'Clan'
    name = forms.CharField(max_length=50, required=False)


class GameResultSearchForm(forms.Form):
    form_name = 'Game'
    date_played = forms.DateField(widget=SelectDateWidget, required=False)


class PlayerSearchForm(forms.Form):
    form_name = 'Player'
    nickname = forms.CharField(max_length=255, required=False)


class TankSearchForm(forms.Form):
    form_name = 'Tank'
    name = forms.CharField(max_length=255, required=False)


class TeamSearchForm(forms.Form):
    form_name = 'Team'
    name = forms.CharField(max_length=255, required=False)
