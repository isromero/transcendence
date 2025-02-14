from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from apps.core.game import process_key_event, left_paddle, right_paddle, ball

@method_decorator(csrf_exempt, name="dispatch")
class GameView(View):
    def get(self, request):
        return JsonResponse({
            "left_paddle": left_paddle,
            "right_paddle": right_paddle,
            "ball": ball
        })

    def post(self, request):
        try:
            data = json.loads(request.body)
            key = data.get("key")
            is_pressed = data.get("is_pressed", False)
            if key:
                process_key_event(key, is_pressed)
                return JsonResponse({"status": "ok"})
            return JsonResponse({"error": "Missing key parameter"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
