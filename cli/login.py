import os
import requests
import websocket
import json
import time

# Game settings (assumed game size: 800×400)
GAME_WIDTH = 800
GAME_HEIGHT = 400

# ASCII canvas settings (including borders)
ASCII_WIDTH = 80
ASCII_HEIGHT = 40

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_game(state, left_username, right_username):
    field_width = ASCII_WIDTH - 2   # leave vertical borders
    field_height = ASCII_HEIGHT - 2  # leave horizontal borders

    scale_x = field_width / GAME_WIDTH
    scale_y = field_height / GAME_HEIGHT

    field = [[' ' for _ in range(field_width)] for _ in range(field_height)]

    lp = state.get("left_paddle", {})
    lp_x = int(lp.get("x", 0) * scale_x)
    lp_y = int(lp.get("y", 0) * scale_y)
    lp_w = max(1, int(lp.get("width", 0) * scale_x))
    lp_h = max(1, int(lp.get("height", 0) * scale_y))
    for i in range(lp_y, min(lp_y + lp_h, field_height)):
        for j in range(lp_x, min(lp_x + lp_w, field_width)):
            field[i][j] = '|'

    rp = state.get("right_paddle", {})
    rp_x = int(rp.get("x", 0) * scale_x)
    rp_y = int(rp.get("y", 0) * scale_y)
    rp_w = max(1, int(rp.get("width", 0) * scale_x))
    rp_h = max(1, int(rp.get("height", 0) * scale_y))
    for i in range(rp_y, min(rp_y + rp_h, field_height)):
        for j in range(rp_x, min(rp_x + rp_w, field_width)):
            field[i][j] = '|'

    ball = state.get("ball", {})
    ball_x = int(ball.get("x", 0) * scale_x)
    ball_y = int(ball.get("y", 0) * scale_y)
    if 0 <= ball_y < field_height and 0 <= ball_x < field_width:
        field[ball_y][ball_x] = 'O'

    canvas_lines = []
    canvas_lines.append("+" + "-" * field_width + "+")
    for row in field:
        canvas_lines.append("|" + "".join(row) + "|")
    canvas_lines.append("+" + "-" * field_width + "+")

    scores = state.get("scores", {"left": 0, "right": 0})
    left_score = scores.get("left", 0)
    right_score = scores.get("right", 0)
    header = f"{left_username}  vs  {right_username}    |    Score: {left_score} - {right_score}"
    
    countdown = state.get("countdown", None)
    if countdown is not None:
        header += f"    |    Countdown: {countdown:.2f}"

    clear_console()
    output = header + "\n" + "\n".join(canvas_lines)
    return output

def login_and_get_cookie(api_url, username, password):
    url = f"{api_url.rstrip('/')}/login"  # Ensure no double slashes
    payload = {"username": username, "password": password}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    session = requests.Session()
    response = session.post(url, json=payload, headers=headers)
    
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

def create_match(api_url, session):
    url = f"{api_url.rstrip('/')}/history"  # Ensure no double slashes
    payload = {"type_match": "local"}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    response = session.post(url, json=payload, headers=headers)
    
    try:
        result = response.json()
    except ValueError:
        print("Invalid JSON response.")
        return None
    
    if not response.ok or not result.get("success", False):
        print("Error:", result.get("error", "Unknown error"))
        return None
    
    print("Match Created:", result)
    return result

def connect_websocket(match_id, left_username, right_username):
    ws_url = f"ws://localhost:8000/ws/game/{match_id}"  # Adjust hostname if needed
    
    def on_message(ws, message):
        try:
            state = json.loads(message)
        except Exception:
            print("Could not parse message as JSON:", message)
            return
        rendered = render_game(state, left_username, right_username)
        print(rendered)
    
    def on_error(ws, error):
        print("WebSocket Error:", error)
    
    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed")
    
    def on_open(ws):
        print("WebSocket connection opened")
    
    from websocket import WebSocketApp
    ws_app = WebSocketApp(ws_url,
                          on_message=on_message,
                          on_error=on_error,
                          on_close=on_close)
    ws_app.on_open = on_open
    ws_app.run_forever()

# Example usage
api_url = "http://localhost:8000/api/"  # Replace with your API URL
username = "testotest"
password = "test1234test!A"
left_username = "Player1"
right_username = "Player2"

session, message, cookies = login_and_get_cookie(api_url, username, password)
if session:
    match_data = create_match(api_url, session)
    if match_data and "data" in match_data:
        match_id = match_data["data"].get("match_id")
        if match_id:
            connect_websocket(match_id, left_username, right_username)
