from django.http import JsonResponse


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        public_paths = [
            "/api/login",
            "/api/register",
            "/api/logout",
            "/api/check-auth",
            "/api/auth/login",
            "/api/auth/token-login",
            "/auth/callback",
            "/auth/login",
            "/auth/login/",
        ]
        print("\n\n REQUEST-->>>", request.path, "\n\n")
        if request.path in public_paths:
            return self.get_response(request)
        if (
            request.path.startswith("/api/")
            and not any(request.path.startswith(path) for path in public_paths)
            and not request.user.is_authenticated
        ):
            return JsonResponse({"error": "Authentication required"}, status=401)
        response = self.get_response(request)
        return response
