from django.http import JsonResponse
from django.views import View
import json
from apps.core.forms.register import RegisterForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import serialize_user
from apps.core.utils import create_response
from apps.core.utils import handle_form_errors
# from apps.core.models import UsedLogin


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if data.get("username") is None or len(data.get("username")) <= 8:
                return create_response(error="Username too short. It must be  9 characters long", status=400)
            # TODO: (jose) borrar código comentado si no se usan los logins de 42 como filtro en el registro
            # if UsedLogin.objects.filter(login=data["username"]).exists():
            #     return create_response(error="Username already in use, please login with 42 intra", status=400)
            form = RegisterForm(data)

            if not form.is_valid():
                return handle_form_errors(form)

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            return create_response(
                data=serialize_user(user), message="Registration successful", status=201
            )

        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)
