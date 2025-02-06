from django.http import JsonResponse
from django.views import View
from django.core.cache import cache
from django.db.models import Q
import json
import logging
from apps.core.forms.login import LoginForm
from django.contrib.auth import authenticate, login
from apps.core.models import User

logger = logging.getLogger(__name__)

class LoginView(View):
    def post(self, request):
        try:
            # Rate limiting
            ip = request.META.get('REMOTE_ADDR')
            attempts_key = f"login_attempts_{ip}"
            attempts = cache.get(attempts_key, 0)

            if attempts >= 5:
                return JsonResponse(
                    {"error": "Too many attempts. Please try again later"}, 
                    status=429
                )

            data = json.loads(request.body)
            form = LoginForm(data)

            if form.is_valid():
                login_field = form.cleaned_data['login']
                password = form.cleaned_data['password']

                # Try to find the user by email or username
                try:
                    user = User.objects.get(
                        Q(username=login_field) | Q(email=login_field)
                    )
                    # Authenticate with the username (Django uses username internally)
                    user = authenticate(
                        username=user.username,
                        password=password
                    )
                except User.DoesNotExist:
                    user = None

                if user:
                    login(request, user)
                    cache.delete(attempts_key)
                    return JsonResponse({"message": "Login successful"}, status=200)
                
                # Increment time with attempts
                cache.set(attempts_key, attempts + 1, 300)  # 5 minutes
                return JsonResponse({"error": "Invalid credentials"}, status=401)

            return JsonResponse({"errors": form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return JsonResponse(
                {"error": "An unexpected error occurred"}, 
                status=500
            )
