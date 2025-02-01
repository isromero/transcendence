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
        user = Friends.objects.filter(user_id=user_)
        return JsonResponse(serialize_friends(user), status=200)
    def post(self, request):
        
