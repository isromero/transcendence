from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class CheckAuthView(View):
    def get(self, request):
        """Check if the user is authenticated for the frontend middleware"""
        if request.user.is_authenticated:
            return JsonResponse({"authenticated": True}, status=200)
        return JsonResponse({"authenticated": False}, status=401)
