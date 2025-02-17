from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from apps.core.models import User

class LoginForm(forms.Form):
    login = forms.CharField(required=True)  # Email or username
    password = forms.CharField(required=True)

    def clean_login(self):
        login = self.cleaned_data.get('login')
        if not login:
            raise forms.ValidationError("Username or email is required")
        return login.lower()

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required")
        return password

    def clean(self):
        cleaned_data = super().clean()
        login = cleaned_data.get('login')
        
        if login:
            # Check if it's email or username
            email_validator = EmailValidator()
            try:
                email_validator(login)
                # It's an email
                if not User.objects.filter(email=login).exists():
                    raise forms.ValidationError("Invalid credentials")
            except forms.ValidationError:
                # It's not an email, so it's a username
                if not User.objects.filter(username=login).exists():
                    raise forms.ValidationError("Invalid credentials")

        return cleaned_data