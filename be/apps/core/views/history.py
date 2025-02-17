from django.http import JsonResponse
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
    def get(self, _, action, **kwargs):
        if "user_id" in kwargs and action == "user":
            user_id = kwargs["user_id"]
            user = get_object_or_404(User, id=user_id)
            user_history = History.objects.filter(user_id=user)
            return JsonResponse(
                {
                    "success": True,
                    "message": "History retrieved successfully",
                    "data": [serialize_history(relation) for relation in user_history],
                },
                status=200,
            )
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request",
            },
            status=400,
        )

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = HistoryForm(data)
            if form.is_valid():
                user = form.save()
                return JsonResponse(
                    {
                        "success": True,
                        "message": "History created successfully",
                        "data": serialize_history(user),
                    },
                    status=201,
                )
            return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    def put(self, request, **kwargs):
        if "history_id" in kwargs:
            history_id = kwargs["history_id"]
            history_instance = get_object_or_404(History, id=history_id)
            try:
                data = json.loads(request.body)
                form = HistoryForm(data, instance=history_instance)
                if form.is_valid():
                    history = form.save()
                    return JsonResponse(
                        {
                            "success": True,
                            "message": "History updated successfully",
                            "data": serialize_history(history),
                        },
                        status=200,
                    )
            except json.JSONDecodeError:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "Invalid JSON",
                    },
                    status=400,
                )
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request",
            },
            status=400,
        )

    def delete(self, _, action=None, **kwargs):
        if "user_id" in kwargs and action == "delete":
            user_id = kwargs["user_id"]
            deleted_count, _ = History.objects.filter(user_id=user_id).delete()

            if deleted_count == 0:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "No history found for this user.",
                    },
                    status=404,
                )

            return JsonResponse(
                {
                    "success": True,
                    "message": f"{deleted_count} history records deleted successfully.",
                },
                status=204,
            )
        elif "history_id" in kwargs and action == None:
            history_id = kwargs["history_id"]
            deleted_count, _ = History.objects.filter(id=history_id).delete()

            if deleted_count == 0:
                return JsonResponse(
                    {
                        "success": False,
                        "message": "No history found for this user.",
                    },
                    status=404,
                )

            return JsonResponse(
                {
                    "success": True,
                    "message": f"{deleted_count} history records deleted successfully.",
                },
                status=204,
            )
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid request",
            },
            status=400,
        )
