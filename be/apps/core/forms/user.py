from django import forms
from django.core.exceptions import ValidationError
import re
from apps.core.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists() and self.instance.email != email:
            raise ValidationError("Email already exists")
        return email.lower()

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if (
            User.objects.filter(username=username).exists()
            and self.instance.username != username
        ):
            raise ValidationError("Username already exists")

        if not re.match("^[a-zA-Z0-9_-]+$", username):
            raise ValidationError(
                "Username can only contain letters, numbers, underscores and hyphens"
            )

        return username.lower()
