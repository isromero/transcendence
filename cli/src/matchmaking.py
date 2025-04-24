import os
import requests
import websocket
import json
import time
import ssl

def login_and_get_cookie(api_url, username, password):
    url = f"{api_url.rstrip('/')}/login"
    payload = {"username": username, "password": password}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    session = requests.Session()
    response = session.post(url, json=payload, headers=headers, verify=False)
    
    try:
        result = response.json()
    except ValueError:
        print("Invalid JSON response.")
        return None, None, None
    
    if not response.ok or not result.get("success", False):
        print("Error:", result.get("error", "Unknown error"))
        return None, None, None
    
    message = result.get("message", "Logged in successfully")
    cookies = session.cookies.get_dict()
    
    print("Success:", message)
    print("Cookies:", cookies)
    
    return session, message, cookies

    # Convert the base URL from https:// to wss:// and append the match path
def matchmaking(cookies, url):
    ws_base = url.replace("https://", "wss://").rstrip("/")
    ws_url = f"{ws_base}/ws/matchmaking"
    result_container = {"match_id": None, "position": None}

    def on_message(ws, message):
        try:
            state = json.loads(message)
        except Exception as e:
            print("Could not parse message as JSON:", message)
            return
        
        # Check for start_match message
        if state.get("type") == "start_match":
            result_container["match_id"] = state.get("match_id")
            result_container["position"] = state.get("position")
            print(f"Match found! ID: {result_container['match_id']}, Player: {result_container['position']}")
            ws.close()
        else:
            print("waiting for other players...")

    def on_error(ws, error):
        print("WebSocket Error:", error)

    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed")

    def on_open(ws):
        print("waiting for other players...")

    cookie_header = '; '.join([f'{key}={value}' for key, value in cookies.items()])
    headers = [f"Cookie: {cookie_header}"]

    from websocket import WebSocketApp
    ws_app = WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header=headers
    )
    ws_app.on_open = on_open
    ws_app.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    return result_container["match_id"], result_container["position"]

# Example usage
'''
api_url = "http://localhost:8000/api/"
username = "testotest"
password = "test1234test!A"
session, message, cookies = login_and_get_cookie(api_url, username, password)

if session:
    match_id, side = connect_websocket(cookies)
    if match_id:
        print(f"Successfully received match_id: {match_id} {side}")
    else:
        print("Did not receive a match_id.")
'''
