# from django.core.cache import cache
import requests
import os
import webbrowser
import json

# cache = {}
# def get_access_token():
#     token = cache.get("42_access_token")
#     if token:
#         return token
#     UID = os.environ.get("UID")
#     API_KEY = os.environ.get("API_KEY")
#     expiration="12/03/2025"
#     auto_regeneration="05/03/2025"
#     REDIRECT="https://www.google.com"

#     data = {
#         "grant_type" : "client_credentials",
#         "client_id" : UID,
#         "client_secret" : API_KEY,
#         }
#     result = requests.post("https://api.intra.42.fr/oauth/token", data=data)
#     if result.status_code == 200:
#         token_data: dict = result.json()
#         access_token = token_data["access_token"]
#         expires_in = token_data.get("expires_in", 7200)
#         # cache.set("42_access_token", access_token, timeout=expires_in-60)
#         cache["42_access_token"] = access_token
#         cache["timeout"] = expires_in-60
#         return access_token
#     else:
#         print(result.status_code, result.text)
#         return None
    
# def user_info(token):
#     if not token:
#         return
#     headers = {
#         "Authorization": f"Bearer {token}"
#     }
#     url = "https://api.intra.42.fr/v2/me"
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         return response.json()  # Devuelve los datos del usuario
#     else:
#         print("Error al obtener la información del usuario:", response.status_code, response.text)
#         return None

def get_access_token_sin_django(auth_code):
    UID = os.environ.get("UID")
    API_KEY = os.environ.get("API_KEY")
    UID="u-s4t2ud-37ff4a4c74679b10b03bab47f05a4d1bc70f63b012fa95a7fefeed85f4996c80"
    API_KEY="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"
    expiration="12/03/2025"
    auto_regeneration="05/03/2025"
    REDIRECT="https://www.google.com"

    data = {
        # "grant_type" : "client_credentials",
        "grant_type" : "authorization_code",
        "client_id" : UID,
        "client_secret" : API_KEY,
        "code" : auth_code,
        "redirect_uri" : REDIRECT,
        }
    result = requests.post("https://api.intra.42.fr/oauth/token", data=data)
    if result.status_code == 200:
        token_data: dict = result.json()
        access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 7200)
        print(access_token, expires_in)
        return access_token
    else:
        print(result.status_code, result.text)
        return None

    

def get_auth_code():
    UID="u-s4t2ud-37ff4a4c74679b10b03bab47f05a4d1bc70f63b012fa95a7fefeed85f4996c80"
    API_KEY="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"
    REDIRECT_URI="https://www.google.com"
    auth_url = f"https://api.intra.42.fr/oauth/authorize?client_id={UID}&redirect_uri={REDIRECT_URI}&response_type=code"
    print("Abre esta URL en tu navegador y autoriza la aplicación:")
    print(auth_url)

    # Abre la URL en el navegador automáticamente
    webbrowser.open(auth_url)

    # Pide al usuario que ingrese el código de autorización manualmente
    auth_code = input("Ingresa el código de autorización que aparece en la URL después de 'code=': ")

    print("Código obtenido:", auth_code)
    return(auth_code)

def user_info(access_token):
    headers = {
        "Authorization" : f"Bearer {access_token}"
    }
    # url = "https://api.intra.42.fr/v2/users/95595/tags_users"
    # url = "https://api.intra.42.fr/v2/users/95595/projects_users"
    url = "https://api.intra.42.fr/v2/me"
    
    # 'user_id': 95595, 'campus_id': 22
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        bonito = json.dumps(data, indent=4)
        with open("bonito.json", "w") as f:
            f.write(bonito)
        return response.json()  # Devuelve los datos del usuario
    else:
        print("Error al obtener la información del usuario:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    auth_code = get_auth_code()
    access_token = get_access_token_sin_django(auth_code)
    user_info(access_token)

    exit(33)
    # print(token)