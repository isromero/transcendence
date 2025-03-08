from django.http import JsonResponse, HttpRequest
from django.views import View
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.core.utils import create_response
from apps.core.models import User
import requests
import json

@method_decorator(csrf_exempt, name="dispatch")
class OAuthLogin(View):
    def post(self, request: HttpRequest):
        # if user is authenticated, return error
        if request.user.is_authenticated:
            return create_response(error="User is already authenticated", status=400)
        try:
            ip = request.META.get("REMOTE_ADDR")
            attempts_key = f"login_attempts_{ip}"
            attempts = cache.get(attempts_key, 0)
            if attempts >= 5:
                return create_response(
                    error="Too many attempts. Please try again later", status=429
                )
            auth_url = (
                f"https://api.intra.42.fr/oauth/authorize?"
                f"client_id={settings.OAUTH42_CLIENT_ID}"
                f"&redirect_uri={settings.OAUTH42_REDIRECT_URI}"
                f"&response_type=code"
                 )
            return redirect(auth_url)
            # return HttpResponse(auth_url) # pendiente de probar después de integrar en el frontend
        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)
        except Exception as e:
            # se peude devolver un error 500???
            return create_response(error="An unexpected error occurred", status=500)

@method_decorator(csrf_exempt, name="dispatch")
class OAuthCallback(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "No authorization code provided"}, status=400)
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.OAUTH42_CLIENT_ID,
            "client_secret": settings.OAUTH42_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.OAUTH42_REDIRECT_URI,
        }
        response = requests.post(settings.OAUTH42_TOKEN_URL, data=data)
        if response.status_code != 200:
            return JsonResponse({"error": "Failed to obtain access token"}, status=400)

        token_data = response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return JsonResponse({"error": "Failed to obtain access token"}, status=400)

        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(settings.OAUTH42_USER_INFO_URL, headers=headers)
        if user_info_response.status_code != 200:
            return JsonResponse({"error": "Failed to obtain user info"}, status=400)

        user_info = user_info_response.json()
        username = user_info.get("login")
        # email = user_info.get("email")
        # user, created = User.objects.get_or_create(username=username, email=email)
        user, created = User.objects.get_or_create(username=username)

        login(request, user)
        response = JsonResponse({"message" : "Login successful"})
        response.set_cookie(
            "sessionid", 
            request.session.session_key, 
            httponly=True, 
            secure=False,
            samesite="Lax",)
        # TODO: aquí hay que redirigir a la página de inicio de la app
        # o devolver la información necesaria para que el frontend redirija
        return response

@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(View):
    def post(self, request:HttpRequest):
        logout(request)
        response = JsonResponse({"message": "Logout successful"})
        response.delete_cookie("sessionid")
        return response

# TODO (jose): eliminar para producción, solo sirve para pruebas con postman
@method_decorator(csrf_exempt, name="dispatch")
class LoginWithToken(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_response(error="No valid access token provided", status=400)
        token = auth_header.split("Bearer ")[1]
        if not token:
            return create_response(error="No access token provided", status=400)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(settings.OAUTH42_USER_INFO_URL, headers=headers)
        if response.status_code != 200:
            return create_response(error="Invalid or expired token", status=401)
        user_data = response.json()
        username = user_data.get("login")
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_unusable_password()
            user.save()
        login(request, user)
        response = create_response(message=f"{username}: Login successful")
        response.set_cookie(
            "sessionid", 
            request.session.session_key, 
            httponly=True, 
            secure=False,
            samesite="Lax",)
        return response
