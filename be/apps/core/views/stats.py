from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import History, User
from apps.core.utils import serialize_stats
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import create_response


@method_decorator(csrf_exempt, name="dispatch")
class StatsView(View):
    def get(self, _, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            user_history = History.objects.filter(user_id=user)
            return create_response(data=serialize_stats(user, user_history))
        except Exception as e:
            return create_response(error=str(e), status=400)
