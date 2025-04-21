from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from apps.core.models import User
from apps.core.utils import validate_username, validate_password


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

        is_username_change = bool(old_username)
        is_password_change = bool(new_password or old_password)

        if not is_username_change and not is_password_change:
            if (
                not cleaned_data.get("username")
                and not cleaned_data.get("oldPassword")
                and not cleaned_data.get("newPassword")
            ):
                raise ValidationError("No changes provided")

        if old_username:
            if not username:
                raise ValidationError(
                    "New username is required when changing username."
                )
            if old_username != self.instance.username:
                raise ValidationError("Old username is incorrect")
            if not password:
                raise ValidationError("Password is required to change username")
            if not check_password(password, self.instance.password):
                raise ValidationError("Password is incorrect")

            validate_username(username)

            if (
                User.objects.filter(username=username.lower()).exists()
                and self.instance.username.lower() != username.lower()
            ):
                raise ValidationError("Username already exists")

            if (
                User.objects.filter(tournament_display_name=username.lower())
                .exclude(pk=self.instance.pk)
                .exists()
            ):
                raise ValidationError(
                    "This username is already taken as a display name by another user."
                )

            if len(username) < 9:
                raise ValidationError("Username must be at least 9 characters long")

        if new_password or old_password:
            submitted_username_for_pwd_change = cleaned_data.get("username")
            if not submitted_username_for_pwd_change:
                raise ValidationError("Username is required to change password")
            if submitted_username_for_pwd_change != self.instance.username:
                raise ValidationError(
                    "Username submitted for password change is incorrect"
                )
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

            validate_password(new_password)

        if old_username and username and username != self.instance.username:
            self.instance.username = username
            self.instance.tournament_display_name = username

        if new_password:
            self.instance.set_password(new_password)

        return cleaned_data
