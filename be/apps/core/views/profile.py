from django.views import View
from apps.core.models import History
from apps.core.utils import serialize_stats_with_history
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import create_response
from django.db import models


@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(View):
    def get(self, request):
        try:
            user = request.user
            user_history = History.objects.filter(
                models.Q(user_id=user) | models.Q(opponent_id=user)
            )
            return create_response(
                data={
                    "id": user.id,
                    "username": user.username,
                    "avatar": user.avatar,
                    "is_online": user.is_online,
                    **serialize_stats_with_history(user, user_history),
                }
            )
        except Exception as e:
            return create_response(error=str(e), status=400)
