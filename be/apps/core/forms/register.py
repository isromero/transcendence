from django import forms
from django.contrib.auth.password_validation import validate_password
from apps.core.models import User
import re


class RegisterForm(forms.ModelForm):
    password_confirmation = forms.CharField()

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not re.match("^[a-zA-Z0-9_-]+$", username):
            raise forms.ValidationError(
                "Username can only contain letters, numbers, underscores and hyphens"
            )

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        return username.lower()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error("password_confirmation", "Passwords do not match")

        if password:
            validate_password(password)

        return cleaned_data
