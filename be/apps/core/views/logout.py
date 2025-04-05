from django.views import View
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import create_response


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(View):
    def post(self, request):
        try:
            logout(request)
            return create_response(message="Logout successful")
        except Exception as e:
            return create_response(
                error=str(e), message="Error during logout", status=500
            )
