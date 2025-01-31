from django.http import JsonResponse, HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from apps.core.models import Stats
from apps.core.utils import serialize_user
from apps.core.forms.user import UserForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name="dispatch")
class StatsView(View):
    def get(self, ):