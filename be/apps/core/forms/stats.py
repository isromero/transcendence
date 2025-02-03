from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import re
from apps.core.models import Stats, User


class StatsForm(forms.ModelForm):
    class Meta:
        model = Stats
        fields = ["user_id", "victories", "defeats", "total_matches", "total_tournaments", "tournaments_victories"]

    def clean_user_id(self):
        user_id = self.cleaned_data.get("user_id")
        if user_id is None:
            raise ValidationError("User with this ID does not exist.")
        return user_id

    def clean_victories(self):
        victories = self.cleaned_data.get("victories")
        if victories is not None and victories < 0:
            raise ValidationError("Victories must be a positive number.")
        return victories

    def clean_defeats(self):
        defeats = self.cleaned_data.get("defeats")
        if defeats is not None and defeats < 0:
            raise ValidationError("Defeats must be a positive number.")
        return defeats

    def clean_total_matches(self):
        total_matches = self.cleaned_data.get("total_matches")
        if total_matches is not None and total_matches < 0:
            raise ValidationError("Total matches must be a positive number.")
        return total_matches

    def clean_total_tournaments(self):
        total_tournaments = self.cleaned_data.get("total_tournaments")
        if total_tournaments is not None and total_tournaments < 0:
            raise ValidationError("Total tournaments must be a positive number.")
        return total_tournaments

    def clean_tournaments_victories(self):
        tournaments_victories = self.cleaned_data.get("tournaments_victories")
        if tournaments_victories is not None and tournaments_victories < 0:
            raise ValidationError("Tournaments victories must be a positive number.")
        return tournaments_victories
