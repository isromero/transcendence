from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views import View
import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import login, logout
# from django.contrib.auth.models import User
from apps.core.models import User
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.core.cache import cache
from apps.core.utils import create_response
import json


class OAuthLogin(View):
    def get(self, request: HttpRequest):
        try:
            # Rate limiting
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


# def auth_login(request: HttpRequest) -> HttpResponse:
#     """Redirige al usuario a la API de 42 para autenticarse"""
#     print("\n\nEstos son los datos de la API de 42: \n\n",
#           settings.OAUTH42_CLIENT_ID, "\n",
#           settings.OAUTH42_REDIRECT_URI, "\n",
#           settings.OAUTH42_TOKEN_URL)
#     auth_url = (
#         f"https://api.intra.42.fr/oauth/authorize?"
#         f"client_id={settings.OAUTH42_CLIENT_ID}"
#         f"&redirect_uri={settings.OAUTH42_REDIRECT_URI}"
#         f"&response_type=code"
#     )
#     return redirect(auth_url)

class OAuthCallback(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        print("AUTH CALLBACK", request.method)
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
        user_id = user_info.get("id")
        email = user_info.get("email")

        user, created = User.objects.get_or_create(username=username, email=email)
        print("\n\nusername:", username, "\nuser_id", user_id, "\nemail", email)
        print("\n\nuser:", user, "\ncreated", created)

        login(request, user)
        csrf_token = get_token(request)
        response = JsonResponse({"message" : "Login successful"})
        response.set_cookie(
            "csrftoken", 
            csrf_token, 
            httponly=False, 
            secure=False,
            samesite="Lax",)
        response.set_cookie(
            "sessionid", 
            request.session.session_key, 
            httponly=True, 
            secure=False,
            samesite="Lax",)
        # aquí hay que redirigir a la página de inicio de la app
        # o devolver la información necesaria para que el frontend redirija
        # return redirect("/auth/wololo")
        return response
        # return redirect("/api/users")       

class LogoutView(View):
    def post(self, request:HttpRequest):
        logout(request)  # Cierra la sesión del usuario
        response = JsonResponse({"message": "Logout successful"})
        response.delete_cookie("sessionid")  # Elimina la cookie de sesión
        response.delete_cookie("csrftoken")  # (Opcional) Elimina la cookie CSRF si se usa
        return response

def auth_logout(request:HttpRequest) -> HttpResponse:
    """Cierra la sesión del usuario"""
    print("Session ID: ", request.COOKIES["sessionid"], 
          "\nCSRF Token: ", request.COOKIES["csrftoken"],
          "\nSession Key: ", request.session.session_key,
          "\nUser: ", request.user)
    # antes de cerrar sesión hay un usuario (request.user==login de 42)
    # antes de cerrar sesión hay una sesión (request.session.session_key==sessionid)
    logout(request)
    # despues de cerrar sesión no hay usuario (request.user==AnonymousUser)
    # despues de cerrar sesión no hay sesión (request.session.session_key==None)
    # pero no cambia ni sessionid ni csrftoken, logout no los modifica
    print("Sesión cerrada:")
    print("Session ID: ", request.COOKIES["sessionid"], 
          "\nCSRF Token: ", request.COOKIES["csrftoken"],
          "\nUser: ", request.user,
          "\nSession Key: ", request.session.session_key)
    
    # aquí hay que redirigir a la ¿página de inicio? de la app
    return HttpResponse("Sesión cerrada. Gracias por participar")
    return redirect("/")

def wololo(request:HttpRequest) -> HttpResponse:
    """Para testear los valores que tiene la request"""
    wololo = ""
    # try:
    #     for key, value in vars(request).items():
    #         print(key, "->", value)
    # except Exception as e:
    #     return HttpResponse("Session ID: " + request.COOKIES["sessionid"] + "<br>" + "CSRF Token: " + request.COOKIES["csrftoken"])
    return HttpResponse("Session ID: " + request.COOKIES["sessionid"] + "<br>" + "CSRF Token: " + request.COOKIES["csrftoken"])
    return HttpResponse(vars(request))

# def auth_callback(request: HttpRequest) -> JsonResponse:
#     """Recibe el código de autorización y obtiene el access token"""
#     print("AUTH CALLBACK", request.method)
#     code = request.GET.get("code")
#     if not code:
#         return JsonResponse({"error": "No authorization code provided"}, status=400)
#     data = {
#         "grant_type": "authorization_code",
#         "client_id": settings.OAUTH42_CLIENT_ID,
#         "client_secret": settings.OAUTH42_CLIENT_SECRET,
#         "code": code,
#         "redirect_uri": settings.OAUTH42_REDIRECT_URI,
#     }
#     response = requests.post(settings.OAUTH42_TOKEN_URL, data=data)
    
#     if response.status_code != 200:
#         return JsonResponse({"error": "Failed to obtain access token"}, status=400)
#     token_data = response.json()
#     access_token = token_data.get("access_token")
#     if not access_token:
#         return JsonResponse({"error": "Failed to obtain access token"}, status=400)
#     headers = {"Authorization": f"Bearer {access_token}"}
#     user_info_response = requests.get(settings.OAUTH42_USER_INFO_URL, headers=headers)
#     if user_info_response.status_code != 200:
#         return JsonResponse({"error": "Failed to obtain user info"}, status=400)
#     user_info = user_info_response.json()
#     username = user_info.get("login")
#     user_id = user_info.get("id")
#     email = user_info.get("email")

#     user, created = User.objects.get_or_create(username=username, email=email)
#     print("\n\nusername:", username, "\nuser_id", user_id, "\nemail", email)
#     print("\n\nuser:", user, "\ncreated", created)

#     login(request, user)
#     csrf_token = get_token(request)
#     response = JsonResponse({"message" : "Login successful"})
#     response.set_cookie(
#         "csrftoken", 
#         csrf_token, 
#         httponly=False, 
#         secure=False,
#         samesite="Lax",)
#     response.set_cookie(
#         "sessionid", 
#         request.session.session_key, 
#         httponly=True, 
#         secure=False,
#         samesite="Lax",)
#     # aquí hay que redirigir a la página de inicio de la app
#     # o devolver la información necesaria para que el frontend redirija
#     # return redirect("/auth/wololo")
#     return response
#     # return redirect("/api/users")