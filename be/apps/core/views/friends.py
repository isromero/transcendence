from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import Friends, User
from apps.core.utils import serialize_user
from apps.core.forms.user import UserForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class FriendsView(View):
    def get(sefl, _, user_id):
        user_ = get_object_or_404(User, id=user_id)
        user_friends = Friends.objects.filter(user_id=user_)
        return JsonResponse(serialize_friends(user_friends), status=200)
    def post(self, request, user_id):
        try:
            data = json.loads(request.body)
            form = FriendForm(data)
            if form.is_valid():
                friend = form.save()
                return JsonResponse(serialize_friend(friend), status=201)
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    def put(self, request):
        user = get_object_or_404(Friends, user_id=user_id)
        try:
            data = json.loads(request.body)
            form = FriendForm(data, instance=user)
            if form.is_valid():
                friend = form.save()
                return JsonResponse(serialize_friend(friend), status=200)
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    def delete(self, user_id, friend_id):
        user = get_object_or_404(Friends, user_id=user_id)
        user_friends = Friends.objects.filter(user_id=user_id, friend_id=friend_id)
        if user_friend.exist():
            user.delete()
            return HttpPesponse(status=204)
