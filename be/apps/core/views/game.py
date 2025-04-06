from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from apps.core.game import GameState


@method_decorator(csrf_exempt, name="dispatch")
class GameView(View):
    game_state = GameState()  # Singleton instance of GameState

    def get(self, _):
        return JsonResponse(self.game_state.get_state())

    def post(self, request):
        try:
            data = json.loads(request.body)
            key = data.get("key")
            is_pressed = data.get("is_pressed", False)

            if key:
                self.game_state.process_key_event(key, is_pressed)
                return JsonResponse({"status": "ok"})
            return JsonResponse({"error": "Missing key parameter"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
