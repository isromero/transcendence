from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import Friends, User


class FriendForm(forms.ModelForm):
    username = forms.CharField(required=True)

    class Meta:
        model = Friends
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        user = User.objects.filter(username=username).first()
        if not user:
            raise ValidationError("Username doesn't exist")

        friend = Friends.objects.filter(
            user_id=self.user.id,
            friend_id=user.id,
        )

        if user == self.user:
            raise ValidationError("You cannot send a friend request to yourself")
        elif friend.filter(status=Friends.Status.ACCEPTED).exists():
            raise ValidationError("You are already friends")
        elif friend.filter(status=Friends.Status.DECLINED).exists():
            raise ValidationError("This user has already declined your friend request")
        elif friend.filter(status=Friends.Status.SENT).exists():
            raise ValidationError("You already sent a friend request to this user")

        self.friend = user
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user_id = self.user
        instance.friend_id = self.friend
        if commit:
            instance.save()
        return instance
