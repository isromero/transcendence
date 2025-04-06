from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from apps.core.game import GameState
from apps.core.utils import create_response


@method_decorator(csrf_exempt, name="dispatch")
class GameView(View):
    game_state = GameState()  # Shared game state instance

    def get(self, _):
        return create_response(data=self.game_state.get_state())

    def post(self, request):
        try:
            data = json.loads(request.body)
            key = data.get("key")
            is_pressed = data.get("is_pressed", False)

            if key:
                self.game_state.process_key_event(key, is_pressed)
                return create_response(message="ok")
            return create_response(error="Missing key parameter", status=400)
        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)
        except Exception as e:
            return create_response(error=str(e), status=500)
