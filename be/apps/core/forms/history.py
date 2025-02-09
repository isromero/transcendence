from django import forms
from django.core.exceptions import ValidationError
from apps.core.models import History, User, Tournaments


class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = "__all__"

    def clean_user_id(self):
        user = self.cleaned_data.get("user_id")
        if not User.objects.filter(id=user.id).exists():
            raise ValidationError("User doesn't exist.")
        return user

    def clean_opponent_id(self):
        opponent = self.cleaned_data.get("opponent_id")
        user = self.cleaned_data.get("user_id")
        if not User.objects.filter(id=opponent.id).exists():
            raise ValidationError("Opponent doesn't exist.")
        elif opponent.id == user.id:
            raise ValidationError("A user cannot be their own opponent.")
        return opponent

    def clean_type_match(self):
        type_match = self.cleaned_data.get("type_match")
        if type_match not in [
            "tournament_quarter",
            "tournament_semi",
            "tournament_final",
            "match",
        ]:
            raise ValidationError("Invalid match type")
        return type_match

    def clean(self):
        cleaned_data = super().clean()
        type_match = cleaned_data.get("type_match")
        if type_match != "match":
            tournament_id = cleaned_data.get("tournament_id")
            position_tournament = cleaned_data.get("position_tournament")
            if (
                tournament_id is None
                or not Tournaments.objects.filter(id=tournament_id.id).exists()
            ):
                raise ValidationError("Tournament doesn't exist.")
            tournament = Tournaments.objects.get(id=tournament_id.id)
            num_players = tournament.players.count()
            if position_tournament and position_tournament > num_players:
                raise ValidationError("Invalid tournament position.")
            if position_tournament is None:
                raise ValidationError("Invalid tournament position.")
        else:
            cleaned_data["position_tournament"] = None
            cleaned_data["tournament_id"] = None
        return cleaned_data
