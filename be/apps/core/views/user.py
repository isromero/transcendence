from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import User, Friends
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
                "id", "username", "email", "avatar", "status"
            )
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

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        try:
            data = json.loads(request.body)
            form = UserForm(data, instance=user)
            if form.is_valid():
                user = form.save()
                return JsonResponse(serialize_user(user), status=200)
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, _, user_id):
        user = get_object_or_404(User, id=user_id)
        user.username = "user_" + str(user.id)
        user.password = ""
        user.avatar = ""#esto hay que buscar
        user.email = time.time() + random.uniform(0.1, 1.0)
        user.status = False
        user.deleted_user = True
        friends = Friends.objects.filter(friend_id=user_id)
        friends.delete()
        user.save(update_fields=['username', 'password', 'avatar', 'email', 'status', 'deleted_user'])
        return HttpResponse(status=204)
