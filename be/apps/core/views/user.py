from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import User, Friends, History, Tournaments
from apps.core.utils import serialize_user, serialize_other_user
from apps.core.forms.user import UserForm
import json
import time
from datetime import datetime, timedelta
import random
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# TODO: @csrf_exempt is a temporary solution to allow the API to be used without CSRF protection.
# TODO: We should use a proper authentication system in the future.


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    def get(self, request: HttpRequest, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
            if request.user.is_authenticated and request.user.id == user_id:
                return JsonResponse({"data": serialize_user(user)}, status=200)
            else:
                return JsonResponse({"data": serialize_other_user(user)}, status=200)
        else:
            users = User.objects.all().values(
                "id", "username", "avatar", "status"
            )#esto hace falta?
            return JsonResponse({"data": list(users)}, status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = UserForm(data)
            if form.is_valid():
                user = form.save()
                return JsonResponse(serialize_user(user), status=201)
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request: HttpRequest, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user.is_authenticated and request.user.id == user_id:
            try:
                data = json.loads(request.body)
                form = UserForm(data, instance=user)
                if form.is_valid():
                    user = form.save()
                    return JsonResponse(serialize_user(user), status=200)
                return JsonResponse({"errors": form.errors}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
        elif not request.user.is_authenticated:
            return JsonResponse({"error": "You do not have permission to modify this user's data."}, status=401)
        else:
            return JsonResponse({"error": "You do not have permission to modify this user's data."}, status=403)
#hay que añadir la comprobacion de que el user que quiere eliminar es el mismo user
    def delete(self, _, user_id):
        user = get_object_or_404(User, id=user_id)
        anon_user, _ = User.objects.get_or_create(username="deleted_user")
        random_numb = time.time() + random.uniform(0.1, 1.0)
        user.password = ""
        user.avatar = ""#esto hay que buscar
        user.email = f"deleted_user_{random_numb}@anon.com"
        user.status = False
        user.deleted_user = True
        #delete user friends
        friends = Friends.objects.filter(user_id=user_id)
        friends.delete()
        #delete user from friend lists
        for friend in Friends.objects.filter(friend_id=user_id):
            friend.friend_id = anon_user
        #delete user history
        history = History.objects.filter(user_id=user_id)
        history.delete()
        #delete the user from other users' history lists
        for history in History.objects.filter(opponent=user_id):
            history.opponent = anon_user
        #delete the user from tournaments
        for tournament in Tournaments.objects.filter(players=user):
            tournament.players.remove(user)
            tournament.players.add(anon_user)
        user.username = "user_" + str(random_numb)
        user.save()
        return JsonResponse({"message": "Your account and all associated data have been permanently deleted."}, status=204)

