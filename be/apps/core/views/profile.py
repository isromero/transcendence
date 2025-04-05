from django.views import View
from apps.core.models import History
from apps.core.utils import serialize_stats
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import create_response


@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(View):
    def get(self, request):
        try:
            user = request.user
            user_history = History.objects.filter(user_id=user)
            return create_response(data=serialize_stats(user, user_history))
        except Exception as e:
            return create_response(error=str(e), status=400)
