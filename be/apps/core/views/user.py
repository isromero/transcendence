from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import User
from apps.core.utils import serialize_user
from apps.core.forms.user import UserForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# TODO: @csrf_exempt is a temporary solution to allow the API to be used without CSRF protection.
# TODO: We should use a proper authentication system in the future.


@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):
    def get(self, _, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
            return JsonResponse(serialize_user(user), status=200)
        else:
            users = User.objects.all().values(
                "id", "username", "email", "avatar", "status"
            )
            return JsonResponse({"users": list(users)}, status=200)

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
        user.delete()
        return HttpResponse(status=204)
