from django import forms
from django.forms import SelectDateWidget


class ClanSearchForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)


class GameResultSearchForm(forms.Form):
    date_played = forms.DateField(widget=SelectDateWidget, required=False)


class PlayerSearchForm(forms.Form):
    nickname = forms.CharField(max_length=255, required=False)


class TankSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)


class TeamSearchForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
