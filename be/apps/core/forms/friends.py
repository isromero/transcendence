from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import Friends

class FriendForm(forms.ModelForm):
    class Meta:
        model = Friends
        fields = ["friend_id"]

    def clean_friend_id(self):
        friend_id = self.cleaned_data.get("friend_id")
        user_id = self.cleaned_data.get("user_id")
        friend = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
        if friend_id = user_id:
            raise ValidationError("Error id")
        elif friend.exist():
            raise ValidationError("Already friends or is sent")
        return friend_id
