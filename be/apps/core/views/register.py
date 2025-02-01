from django.http import JsonResponse
from django.views import View
from django.contrib.auth import get_user_model
import json
from apps.core.forms.register import RegisterForm

User = get_user_model()


class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            form = RegisterForm(data)

            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.save()
                return JsonResponse(
                    {"message": "User registered successfully"}, status=201
                )

            return JsonResponse({"errors": form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
