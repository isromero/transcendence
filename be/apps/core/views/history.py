from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import History
from apps.core.utils import serialize_history
from apps.core.forms.history import HistoryForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class HistoryView(View):
    def get(self, _, user_id):
        user = get_object_or_404(User, id=user_id)
        return JsonResponse(serialize_history(user), status=200)

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = HistoryForm(data)
            if form.is_valid():
                user = form.save()
                return JsonResponse(serialize_history(user), status=201)
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        try:
            data = json.loads(request.body)
            form = HistoryForm(data, instance=user)
            if form.is_valid():
                user = form.save()
                return JsonResponse(serialize_history(user), status=200)
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def delete(self, _, user_id):
        user = get_object_or_404(History, id=user_id)
        user.delete()
        return HttpResponse(status=204)
