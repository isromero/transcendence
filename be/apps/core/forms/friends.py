from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import Friends, User


class FriendForm(forms.ModelForm):
    username = forms.CharField(required=True)

    class Meta:
        model = Friends
        fields = []

    # TODO: This is not working bcs we need to get the user from request...
    # TODO: I don't have internet know so don't know how to get it
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        user = User.objects.filter(username=username)
        if not user:
            raise ValidationError("Username doesn't exist")

        friend = Friends.objects.filter(
            user_id=self.user.id,
            friend_id=user.id,
        )

        if user == self.user:
            raise ValidationError("You cannot send a friend request to yourself")
        elif friend.exists():
            raise ValidationError("You are already friends")

        return cleaned_data
