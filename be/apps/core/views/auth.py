from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
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
import os

@method_decorator(csrf_exempt, name="dispatch")
class OAuthLogin(View):
    def get(self, request: HttpRequest):
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
        except json.JSONDecodeError:
            return create_response(error="Invalid JSON", status=400)
        except Exception as e:
            return create_response(error="An unexpected error occurred", status=500)


@method_decorator(csrf_exempt, name="dispatch")
class OAuthCallback(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "No authorization code provided"}, status=400)
        token_data = self.exchange_code_for_token(code)
        if "error" in token_data:
            return JsonResponse(token_data, status=400)
        user_info = self.get_user_info(token_data.get("access_token"))
        if "error" in user_info:
            return JsonResponse(user_info, status=400)
        self.response = self.authenticate_and_login(request, user_info)
        self.redirect_response = HttpResponseRedirect(f"http://localhost:3001/")
        # self.redirect_response = HttpResponseRedirect(f"http://{os.uname().nodename.split('.')[0]}:3001/")
        self.transfer_data()
        return self.redirect_response
    
    def transfer_data(self):
        for key, value in self.response.items():
            self.redirect_response.set_cookie(key, value)

    def exchange_code_for_token(self, code: str) -> dict:
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.OAUTH42_CLIENT_ID,
            "client_secret": settings.OAUTH42_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.OAUTH42_REDIRECT_URI,
        }
        api_response = requests.post(settings.OAUTH42_TOKEN_URL, data=data)
        if api_response.status_code != 200:
            return {"error": "Failed to obtain access token"}
        return api_response.json()
    
    def get_user_info(self, access_token: str) -> dict:
        if not access_token:
            return {"error": "Invalid access token"}
        headers = {"Authorization": f"Bearer {access_token}"}
        api_response = requests.get(settings.OAUTH42_USER_INFO_URL, headers=headers)
        if api_response.status_code != 200:
            return {"error": "Failed to obtain user information"}
        return api_response.json()

    def authenticate_and_login(self, request: HttpRequest, user_info: dict) -> JsonResponse:
        username = user_info.get("login")
        if not username:
            return JsonResponse({"error": "Invalid user information"}, status=400)
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_unusable_password()
        user.is_online = True
        user.save()
        login(request, user)
        response = JsonResponse({"message": f"{username}: Login successful"})
        response.set_cookie(
            "sessionid", 
            request.session.session_key, 
            httponly=True, 
            secure=False,
            samesite="Lax",)
        return response
    

@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(View):
    def post(self, request:HttpRequest):
        print("\n\n ->->->->->-<>_>_>_>_>_>        LOGOUT        <-<-<-<-<-<-<-<-<-\n\n")
        user = request.user
        user.is_online = False
        user.save(update_fields=["is_online"])
        logout(request)
        response = JsonResponse({"message": "Logout successful"})
        response.delete_cookie("sessionid")
        return response
        # redirect_response = HttpResponseRedirect("http://localhost:3001/")
        # redirect_response.delete_cookie("sessionid")
        # return redirect_response


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
        user.is_online = True
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
