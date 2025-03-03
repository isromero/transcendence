from django.http import JsonResponse


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO (ismael): delete /api/game and /ws/game when finished
        public_paths = ["/api/login", "/api/register", "/api/game", "/ws/game",
                        "/api/auth/login"]

        if (
            request.path.startswith("/api/")
            and not any(request.path.startswith(path) for path in public_paths)
            and not request.user.is_authenticated
        ):
            return JsonResponse({"error": "Authentication required"}, status=401)

        response = self.get_response(request)
        return response
