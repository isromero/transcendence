from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import Tournaments

class TournamentsForm(forms.ModelForm):
    class Meta:
        model = Tournaments
        fields = ["tournament_name", "players"]

    def clean_tournament_name(self):
        tournament_name = self.cleaned.data.get("tournament_name")
        if (
            Tournaments.objects.filter(tournament_name=tournament_name).exists()
            and self.instance.tournament_name != tournament_name
        ):
            raise ValidationError("Tournament name already exists")
        if not re.match("^[a-zA-Z0-9_-]+$", tournament_name):
            raise ValidationError(
                "Tournament name can only contain letters, numbers, underscores and hyphens"
            )
    def clean_date(self):
        start_date = self.cleaned.data.get("start_date")
        end_date = self.cleaned.data.get("end_date")
        if start_date > datetime.now():
            raise ValidationError ("The start date is invalid.")
        if staend_datert_date > datetime.now():
            raise ValidationError ("The end date is invalid.")
    def clean_players(self):
        players = self.cleaned_data.get("players")
        if players.count() < 4:
            raise ValidationError ("Insufficient players.")
        if players.count() > 16:
            raise ValidationError ("Too many players.")
        if players.count() % 2 != 0:
            raise ValidationError ("The number of players must be even.")
        if len(set(players)) != len(players):
            raise ValidationError ("There are duplicate players.")

class TournamentsPutForm(forms.ModelForm):
    class Meta:
        model = Tournaments
        fields = ["tournament_name", "players"]

    def clean_date(self):
        start_date = self.cleaned.data.get("start_date")
        end_date = self.cleaned.data.get("end_date")
        if start_date > datetime.now():
            raise ValidationError ("The start date is invalid.")
        if staend_datert_date > datetime.now():
            raise ValidationError ("The end date is invalid.")
    def clean_players(self):
        players = self.cleaned_data.get("players")
        if players.count() < 4:
            raise ValidationError ("Insufficient players.")
        if players.count() > 16:
            raise ValidationError ("Too many players.")
        if players.count() % 2 != 0:
            raise ValidationError ("The number of players must be even.")
        if len(set(players)) != len(players):
            raise ValidationError ("There are duplicate players.")
