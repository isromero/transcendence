from django.views import View
from django.core.cache import cache
import json
from apps.core.forms.login import LoginForm
from django.contrib.auth import authenticate, login
from apps.core.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from apps.core.utils import serialize_user
from apps.core.utils import create_response
from apps.core.utils import handle_form_errors


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        try:
            # Rate limiting
            ip = request.META.get("REMOTE_ADDR")
            attempts_key = f"login_attempts_{ip}"
            attempts = cache.get(attempts_key, 0)

            if attempts >= 5:
                return create_response(
                    error="Too many attempts. Please try again later", status=429
                )

            data = json.loads(request.body)
            form = LoginForm(data)

            if not form.is_valid():
                return handle_form_errors(form)

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                user = User.objects.get(username=username)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                user = None

            if user:
                login(request, user)
                cache.delete(attempts_key)
                return create_response(
                    data=serialize_user(user), message="Login successful"
                )

            cache.set(attempts_key, attempts + 1, 300)
            return create_response(error="Invalid credentials", status=401)

        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)
        except Exception as e:
            return create_response(error="An unexpected error occurred", status=500)
