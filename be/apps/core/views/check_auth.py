from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import create_response


@method_decorator(csrf_exempt, name="dispatch")
class CheckAuthView(View):
    def get(self, request):
        """Check if the user is authenticated for the frontend middleware"""
        if request.user.is_authenticated:
            return create_response(data={"authenticated": True}, status=200)
        return create_response(data={"authenticated": False}, status=401)
