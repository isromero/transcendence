from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import Tournaments, History

class TournamentsForm(forms.ModelForm):
    class Meta:
        model = Tournaments
        fields = ["tournament_name", "max_players"]

    def clean_tournament_name(self):
        tournament_name = self.cleaned_data.get("tournament_name")
        if not tournament_name:
            raise ValidationError("Tournament name is required")
            
        if Tournaments.objects.filter(tournament_name=tournament_name).exists():
            raise ValidationError("Tournament name already exists")
            
        if not re.match("^[a-zA-Z0-9_-]{3,50}$", tournament_name):
            raise ValidationError(
                "Tournament name must be 3-50 characters and can only contain letters, numbers, underscores and hyphens"
            )
        return tournament_name
    
    def clean_max_players(self):
        max_players = self.cleaned_data.get("max_players")
        if not max_players:
            raise ValidationError("Max players is required")
            
        if max_players not in [4, 6, 8]:
            raise ValidationError("Tournament must have 4, 6 or 8 players")
            
        return max_players