from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import Friends


class FriendForm(forms.ModelForm):
    class Meta:
        model = Friends
        fields = ["friend_id", "user_id"]

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get("user_id")
        friend_id = cleaned_data.get("friend_id")
        friend = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
        if user_id == friend_id:
            raise ValidationError("Error id")
        elif friend.exists():
            raise ValidationError("Already friends or is sent")
        return cleaned_data
