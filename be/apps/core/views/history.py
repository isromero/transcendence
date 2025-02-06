from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import History, User
from apps.core.utils import serialize_history
from apps.core.forms.history import HistoryForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class HistoryView(View):
    def get(self, _, user_id):
        user = get_object_or_404(User, id=user_id)
        user_history = History.objects.filter(user_id=user)
        return JsonResponse(
            {"data": [serialize_history(relation) for relation in user_history]},
            status=200,
        )
        #return JsonResponse(serialize_history(user), status=200)

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
        deleted_count, _ = History.objects.filter(user_id=user_id).delete()
    
        if deleted_count == 0:
            return JsonResponse({"error": "No history found for this user."}, status=404)

        return JsonResponse({"message": f"{deleted_count} history records deleted successfully."}, status=204)
        # user = get_object_or_404(History, user_id=user_id)
        # user.delete()
        # return HttpResponse(status=204)
