from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import Stats


class StatsForm(forms.ModelForm):
    class Meta:
        model = Stats

    def clean_victories(self):
        victories = self.cleaned_data.get("victories")
        if victories.exist():
            if victories < 0:
                raise ValidationError("Victories must be a positive number.")
            if not isinstance(victories, (int)):
                raise ValidationError("Victories must be a number.")
            
     def clean_defeats(self):
        defeats = self.cleaned_data.get("defeats")
        if defeats.exist():
            if defeats < 0:
                raise ValidationError("Defeats must be a positive number.")
            if not isinstance(defeats, (int)):
                raise ValidationError("Defeats must be a number.")
            
     def clean_total_matches(self):
        total_matches = self.cleaned_data.get("total_matches")
        if total_matches.exist():
            if total_matches < 0:
                raise ValidationError("Total matches must be a positive number.")
            if not isinstance(total_matches, (int)):
                raise ValidationError("Total  matches must be a number.")
            
     def clean_total_tournaments(self):
        total_tournaments = self.cleaned_data.get("total_tournaments")
        if total_tournaments.exist():
            if total_tournaments < 0:
                raise ValidationError("Totalt ournaments must be a positive number.")
            if not isinstance(total_tournaments, (int)):
                raise ValidationError("Total tournaments must be a number.")
            
     def clean_tournaments_victories(self):
        tournaments_victories = self.cleaned_data.get("tournaments_victories")
        if tournaments_victories.exist():
            if tournaments_victories < 0:
                raise ValidationError("Tournaments victories must be a positive number.")
            if not isinstance(tournaments_victories, (int)):
                raise ValidationError("Tournaments victories must be a number.")
