from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from apps.core.game import process_key_event, left_paddle, right_paddle, ball  # Importar la lógica de juego

@method_decorator(csrf_exempt, name="dispatch")
class GameView(View):
    def get(self, request):
        """ Devuelve el estado actual del juego """
        return JsonResponse({
            "left_paddle": left_paddle,
            "right_paddle": right_paddle,
            "ball": ball
        }, status=200)

    def post(self, request):
        """ Recibe eventos de teclado desde el frontend """
        try:
            data = json.loads(request.body)
            key = data.get("key")
            is_pressed = data.get("is_pressed", False)
            if key:
                process_key_event(key, is_pressed)
                return JsonResponse({"status": "ok"}, status=200)
            return JsonResponse({"error": "Missing key parameter"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
