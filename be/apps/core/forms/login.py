from django import forms
from apps.core.models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Username is required")
        return username.lower()

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password is required")
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Invalid credentials")

        return cleaned_data
