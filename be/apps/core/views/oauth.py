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
from urllib.parse import urlparse
import uuid


@method_decorator(csrf_exempt, name="dispatch")
class OAuthLogin(View):
    def get(self, request: HttpRequest):
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
            return create_response(error="No authorization code provided", status=400)
        token_data = self._exchange_code_for_token(code)
        if "error" in token_data:
            return create_response(error=token_data, status=400)
        user_info = self._get_user_info(token_data.get("access_token"))
        if "error" in user_info:
            return create_response(error=user_info, status=400)
        self._authenticate_and_login(request, user_info)
        self._transfer_data(user_info, token_data)
        return HttpResponseRedirect(f"https://{settings.OAUTH42_HOSTNAME}/")

    def _download_and_save_avatar(self, avatar_url):
        """Download avatar from 42 CDN and save it locally"""
        try:
            # If the URL is from 42 CDN, download and save locally
            if "cdn.intra.42.fr" in avatar_url:
                response = requests.get(avatar_url)
                if response.status_code == 200:
                    # Generate unique name for the file
                    file_extension = os.path.splitext(urlparse(avatar_url).path)[1]
                    filename = f"avatar_{uuid.uuid4()}{file_extension}"
                    file_path = os.path.join(settings.MEDIA_ROOT, filename)

                    # Save image directly in media
                    with open(file_path, "wb") as f:
                        f.write(response.content)

                    return filename

            return f"/{avatar_url}"
        except Exception as e:
            print(f"Error downloading avatar: {e}")
            return "default_avatar.webp"

    def _transfer_data(self, user_info, token_data):
        """Transfer user data from 42 API to our database"""
        try:
            try:
                # If the user exists, only update tokens
                user = User.objects.get(username=user_info["login"])
                user.access_token = token_data["access_token"]
                user.refresh_token = token_data["refresh_token"]
                user.save()
                return user
            except User.DoesNotExist:
                # If it's a new user, download the avatar
                avatar_url = user_info["image"]["link"]
                local_avatar_path = self._download_and_save_avatar(avatar_url)
                return User.objects.create(
                    username=user_info["login"],
                    avatar=local_avatar_path,
                    access_token=token_data["access_token"],
                    refresh_token=token_data["refresh_token"],
                )
        except Exception as e:
            print(f"Error in _transfer_data: {e}")
            return None

    def _exchange_code_for_token(self, code: str) -> dict:
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

    def _get_user_info(self, access_token: str) -> dict:
        if not access_token:
            return {"error": "Invalid access token"}
        headers = {"Authorization": f"Bearer {access_token}"}
        api_response = requests.get(settings.OAUTH42_USER_INFO_URL, headers=headers)
        if api_response.status_code != 200:
            return {"error": "Failed to obtain user information"}
        return api_response.json()

    def _authenticate_and_login(
        self, request: HttpRequest, user_info: dict
    ) -> JsonResponse:
        username = user_info.get("login")
        if not username:
            return create_response(error="Invalid user information", status=400)
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
            samesite="Lax",
        )
        return response


# ! Only use for testing with Postman/Other tools
# @method_decorator(csrf_exempt, name="dispatch")
# class LoginWithToken(View):
#     def post(self, request: HttpRequest) -> JsonResponse:
#         auth_header = request.headers.get("Authorization")
#         if not auth_header or not auth_header.startswith("Bearer "):
#             return create_response(error="No valid access token provided", status=400)
#         token = auth_header.split("Bearer ")[1]
#         if not token:
#             return create_response(error="No access token provided", status=400)
#         headers = {"Authorization": f"Bearer {token}"}
#         response = requests.get(settings.OAUTH42_USER_INFO_URL, headers=headers)
#         if response.status_code != 200:
#             return create_response(error="Invalid or expired token", status=401)
#         user_data = response.json()
#         username = user_data.get("login")
#         user, created = User.objects.get_or_create(username=username)
#         if created:
#             user.set_unusable_password()
#         user.save()
#         login(request, user)
#         response = create_response(message=f"{username}: Login successful")
#         response.set_cookie(
#             "sessionid",
#             request.session.session_key,
#             httponly=True,
#             secure=False,
#             samesite="Lax",
#         )
#         return response