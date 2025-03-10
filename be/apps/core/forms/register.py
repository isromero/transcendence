from django import forms
from apps.core.models import User
from apps.core.utils import validate_username, validate_password


class RegisterForm(forms.ModelForm):
    password_confirmation = forms.CharField()

    class Meta:
        model = User
        fields = ["username", "password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        validated_username = validate_username(username)

        if User.objects.filter(username=validated_username).exists():
            raise forms.ValidationError("Username already exists")

        return validated_username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error("password_confirmation", "Passwords do not match")

        if password:
            validate_password(password)

        return cleaned_data
