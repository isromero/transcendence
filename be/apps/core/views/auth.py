from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views import View
import requests
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def auth_login(request: HttpRequest) -> HttpResponse:
    """Redirige al usuario a la API de 42 para autenticarse"""
    print("\n\nEstos son los datos de la API de 42: \n\n",
          settings.OAUTH42_CLIENT_ID, 
          settings.OAUTH42_REDIRECT_URI, 
          settings.OAUTH42_TOKEN_URL)
    auth_url = (
        f"https://api.intra.42.fr/oauth/authorize?"
        f"client_id={settings.OAUTH42_CLIENT_ID}"
        f"&redirect_uri={settings.OAUTH42_REDIRECT_URI}"
        f"&response_type=code"
    )
    return redirect(auth_url)

def auth_callback(request: HttpRequest):
    """Recibe el código de autorización y obtiene el access token"""
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
    print(username, user_id)

    user, created = User.objects.get_or_create(username=username, email=email)

    login(request, user)

    return redirect("/auth/wololo")
    # return redirect("/api/users")

def auth_logout(request:HttpRequest) -> HttpResponse:
    """Cierra la sesión del usuario"""
    logout(request)
    print("Sesión cerrada")
    return HttpResponse("Sesión cerrada. Gracias por participar")
    return redirect("/")

def wololo(request:HttpRequest) -> HttpResponse:
    """Para testear los valores que tiene la request"""
    wololo = ""
    # for key, value in vars(request).items():
    #     print(key, "->", value)
    return HttpResponse(vars(request))