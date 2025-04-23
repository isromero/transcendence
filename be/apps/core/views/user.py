from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import User, Friends, History
from apps.core.utils import serialize_user, create_response
from apps.core.forms.user import UserForm
import json
import time
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout, authenticate
import os
from django.conf import settings
from apps.core.utils import handle_form_errors

# TODO: @csrf_exempt is a temporary solution to allow the API to be used without CSRF protection.
# TODO: We should use a proper authentication system in the future.


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    def get(self, _, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
            return create_response(data=serialize_user(user))
        else:
            users = User.objects.all()
            return create_response(
                data=[serialize_user(user) for user in users],
            )

    def put(self, request):
        try:
            data = json.loads(request.body)

            form = UserForm(data, instance=request.user)
            if form.is_valid():
                user = form.save()
                # If the user changed the password, log them in again to maintain the session
                if data.get("newPassword"):
                    login(request, user)
                return create_response(
                    data=serialize_user(user), message="User updated successfully"
                )
            return handle_form_errors(form)
        except json.JSONDecodeError:
            return create_response(
                error="Invalid JSON", message="User update failed", status=400
            )

    def delete(self, request):
        try:
            data = json.loads(request.body)
            password = data.get("password")

            if len(request.user.username) < 9:
                return self.delete_user(request.user, request)

            if not password:
                return create_response(
                    error="Password is required",
                    message="Please provide your password to confirm deletion",
                    status=400,
                )

            user = authenticate(username=request.user.username, password=password)
            if not user:
                return create_response(
                    error="Invalid password",
                    message="The password is incorrect",
                    status=400,
                )

            return self.delete_user(user, request)

        except json.JSONDecodeError:
            return create_response(
                error="Invalid JSON",
                message="The request body must be valid JSON",
                status=400,
            )
        except Exception as e:
            return create_response(
                error=str(e), message="Error deleting account", status=500
            )

    def delete_user(self, user, request):
        """Anonymize user data and delete user"""
        # Anonymize user data
        user.password = ""
        user.avatar = "/images/default_avatar.webp"
        user.deleted_user = True
        user.username = f"anonymized_user_{user.id}"
        user.tournament_display_name = f"anonymized_user_{user.id}"

        # Delete friends
        Friends.objects.filter(user_id=user.id).delete()
        Friends.objects.filter(friend_id=user.id).update(friend_id=user)

        # Delete history
        History.objects.filter(user_id=user.id).delete()

        user.save()
        logout(request)

        return create_response(
            message="Your account and all associated data have been permanently deleted.",
            status=204,
        )

    # For uploading an avatar
    def post(self, request):
        try:
            avatar = request.FILES.get("avatar")
            if not avatar:
                return create_response(
                    error="No file provided",
                    message="Please provide an avatar image",
                    status=400,
                )

            if not avatar.content_type.startswith("image/"):
                return create_response(
                    error="Invalid file type",
                    message="Please provide an image file",
                    status=400,
                )

            if avatar.size > 5 * 1024 * 1024:  # 5MB
                return create_response(
                    error="File too large",
                    message="Avatar size should be less than 5MB",
                    status=400,
                )

            filename = f"avatar_{request.user.id}_{int(time.time())}{os.path.splitext(avatar.name)[1]}"
            filepath = os.path.join(settings.MEDIA_ROOT, filename)

            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            with open(filepath, "wb+") as destination:
                for chunk in avatar.chunks():
                    destination.write(chunk)

            user = request.user
            user.avatar = f"/images/{filename}"
            user.save()

            return create_response(
                data=serialize_user(user), message="Avatar updated successfully"
            )

        except Exception as e:
            return create_response(
                error=str(e), message="Error updating avatar", status=500
            )
