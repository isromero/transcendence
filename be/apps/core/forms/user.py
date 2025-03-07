from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
import re
from apps.core.models import User


class UserForm(forms.ModelForm):
    oldUsername = forms.CharField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)
    oldPassword = forms.CharField(required=False)
    newPassword = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["username"]

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        old_username = cleaned_data.get("oldUsername")
        password = cleaned_data.get("password")
        old_password = cleaned_data.get("oldPassword")
        new_password = cleaned_data.get("newPassword")

        # If there are no changes
        if not username and not old_password and not new_password:
            raise ValidationError("No changes provided")

        # Validate username change
        if username:
            # Only validate old_username if we are changing the username
            if username.lower() != self.instance.username.lower():
                if not old_username:
                    raise ValidationError("Old username is required")
                if old_username.lower() != self.instance.username.lower():
                    raise ValidationError("Old username is incorrect")
                if not password:
                    raise ValidationError("Password is required to change username")
                if not check_password(password, self.instance.password):
                    raise ValidationError("Password is incorrect")

            # Username registration validations
            if not re.match("^[a-zA-Z0-9_-]+$", username):
                raise ValidationError(
                    "Username can only contain letters, numbers, underscores and hyphens"
                )
            if len(username) < 3:
                raise ValidationError("Username must be at least 3 characters long")
            if len(username) > 20:
                raise ValidationError("Username must be at most 20 characters long")

            # Check if the new username already exists
            if (
                User.objects.filter(username=username.lower()).exists()
                and self.instance.username.lower() != username.lower()
            ):
                raise ValidationError("Username already exists")

        # Validate password change
        if new_password or old_password:
            if not old_password:
                raise ValidationError("Old password is required to set a new password")
            if not new_password:
                raise ValidationError("New password is required")
            if not check_password(old_password, self.instance.password):
                raise ValidationError("Old password is incorrect")
            if new_password == old_password:
                raise ValidationError(
                    "New password must be different from old password"
                )

            # Password registration validations
            if len(new_password) < 8:
                raise ValidationError("Password must be at least 8 characters long")
            if len(new_password) > 128:
                raise ValidationError("Password must be at most 128 characters long")
            if not re.search("[A-Z]", new_password):
                raise ValidationError(
                    "Password must contain at least one uppercase letter"
                )
            if not re.search("[a-z]", new_password):
                raise ValidationError(
                    "Password must contain at least one lowercase letter"
                )
            if not re.search("[0-9]", new_password):
                raise ValidationError("Password must contain at least one number")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get("newPassword"):
            user.set_password(self.cleaned_data["newPassword"])

        if commit:
            user.save()

        return user
