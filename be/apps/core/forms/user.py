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

        # If there are no changes
        if not username and not old_password and not new_password:
            raise ValidationError("No changes provided")

        # Validate username change - only if oldUsername is provided
        if old_username:
            if old_username != self.instance.username:
                raise ValidationError("Username is incorrect")
            if not password:
                raise ValidationError("Password is required to change username")
            if not check_password(password, self.instance.password):
                raise ValidationError("Password is incorrect")

            # Validate the new username
            validate_username(username)

            # Verify if the new username already exists
            if (
                User.objects.filter(username=username.lower()).exists()
                and self.instance.username.lower() != username.lower()
            ):
                raise ValidationError("Username already exists")

        # Verify password change
        if new_password or old_password:
            if not username:
                raise ValidationError("Username is required to change password")
            if username != self.instance.username:
                raise ValidationError("Username is incorrect")
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

            # Validate new password
            validate_password(new_password)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Always keep the current username if no new one is provided
        if "username" not in self.cleaned_data:
            user.username = self.instance.username

        if self.cleaned_data.get("newPassword"):
            user.set_password(self.cleaned_data["newPassword"])

        if commit:
            user.save()

        return user
