from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import User, Friends, History, Tournaments
from apps.core.utils import serialize_user, create_response
from apps.core.forms.user import UserForm
import json
import time
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.templatetags.static import static
from django.contrib.auth import login

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
        if not request.user.is_authenticated:
            return create_response(
                error="Authentication required",
                message="Please log in to update your profile",
                status=401,
            )

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
            return create_response(
                error=form.errors, message="User update failed", status=400
            )
        except json.JSONDecodeError:
            return create_response(
                error="Invalid JSON", message="User update failed", status=400
            )

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user.id == user_id:
            anon_user, _ = User.objects.get_or_create(username="deleted_user")
            random_numb = time.time() + random.uniform(0.1, 1.0)
            user.password = ""
            user.avatar = static("default_avatar.webp")
            user.is_online = False
            user.deleted_user = True

            # Delete user friends
            friends = Friends.objects.filter(user_id=user_id)
            friends.delete()
            # Delete user from friend lists
            for friend in Friends.objects.filter(friend_id=user_id):
                friend.friend_id = anon_user

            # TODO (ismael): I think this is bad bcs we need to anonymize the history of the user
            # Delete user history
            history = History.objects.filter(user_id=user_id)
            history.delete()

            # Anonymize the user from other users' history lists
            for history in History.objects.filter(opponent_id=user_id):
                history.opponent_id = anon_user

            # Anonymize the user from tournaments
            for tournament in Tournaments.objects.filter(players=user):
                tournament.players.remove(user)
                tournament.players.add(anon_user)
            user.username = "anonymized_user_" + str(user.id)
            user.save()
            return JsonResponse(
                {
                    "message": "Your account and all associated data have been permanently deleted."
                },
                status=204,
            )
        else:
            return JsonResponse(
                {"error": "You do not have permission to delete this user's data."},
                status=403,
            )
