from django.http import JsonResponse
from django.utils import timezone


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        public_paths = [
            "/api/login",
            "/api/register",
            "/api/logout",
            "/api/check-auth",
        ]

        if (
            request.path.startswith("/api/")
            and not any(request.path.startswith(path) for path in public_paths)
            and not request.user.is_authenticated
        ):
            return JsonResponse({"error": "Authentication required"}, status=401)

        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.save(update_fields=["last_activity"])

        response = self.get_response(request)
        return response
