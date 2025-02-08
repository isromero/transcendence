from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import Stats, History, User
from apps.core.utils import serialize_stats
from apps.core.forms.stats import StatsForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class StatsView(View):
    def get(self, _, user_id):
        user = get_object_or_404(User, id=user_id)
        user_history = History.objects.filter(user_id=user, position_match=1)
        return JsonResponse(serialize_stats(user), status=200)

    # def post(self, request):
    #     try:
    #         data = json.loads(request.body)
    #         form = StatsForm(data)
    #         if form.is_valid():
    #             user = form.save()
    #             return JsonResponse(serialize_stats(user), status=201)
    #         return JsonResponse({"errors": form.errors}, status=400)
    #     except json.JSONDecodeError:
    #         return JsonResponse({"error": "Invalid JSON"}, status=400)

    # def put(self, request, user_id):
    #     user = get_object_or_404(Stats, user_id=user_id)
    #     try:
    #         data = json.loads(request.body)
    #         form = StatsForm(data, instance=user)
    #         if form.is_valid():
    #             user = form.save()
    #             return JsonResponse(serialize_stats(user), status=200)
    #         return JsonResponse({"errors": form.errors}, status=400)
    #     except json.JSONDecodeError:
    #         return JsonResponse({"error": "Invalid JSON"}, status=400)

    # def delete(self, _, user_id):
    #     user = get_object_or_404(Stats, user_id=user_id)
    #     user.delete()
    #     return HttpResponse(status=204)