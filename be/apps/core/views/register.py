from django.http import JsonResponse
from django.views import View
import json
from apps.core.forms.register import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import serialize_user
from apps.core.utils import create_response
from apps.core.utils import handle_form_errors


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            form = RegisterForm(data)

            if not form.is_valid():
                print("\n\n--- Form Errors ---\n", form.errors, "\n\n")
                return handle_form_errors(form)

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            return create_response(
                data=serialize_user(user), message="Registration successful", status=201
            )

        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)
