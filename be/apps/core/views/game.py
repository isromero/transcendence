from django.http import JsonResponse

def start_game(request):
    return JsonResponse({"message": "Juego iniciado", "status": "ok"})

def get_game_state(request):
    return JsonResponse({"ball_position": [50, 50], "paddle_positions": [40, 60]})
