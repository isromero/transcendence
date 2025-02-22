from django.http import JsonResponse


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def _call_(self, request):
        public_paths = [
            "/api/login",
            "/api/register",
            "/api/history",
            "/api/history/match",
        ]

        if (
            request.path.startswith("/api/")
            and not any(request.path.startswith(path) for path in public_paths)
            and not request.user.is_authenticated
        ):
            return JsonResponse({"error": "Authentication required"}, status=401)

        response = self.get_response(request)
        return response
