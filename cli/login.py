import os
import requests
import websocket
import json
import time
import threading
import sys
import termios
import tty
import select
from src.render import render

# Game settings (assumed game size: 800×400)
GAME_WIDTH = 800
GAME_HEIGHT = 400

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_game(state, left_username, right_username):
    # Left paddle
    left_paddle = state.get("left_paddle", {})
    left_paddle_x = int(left_paddle.get("x", 0))
    left_paddle_y = int(left_paddle.get("y", 0))
    left_paddle_width = left_paddle.get("width", 0)
    left_paddle_height = left_paddle.get("height", 0)

    # Right paddle
    right_paddle = state.get("right_paddle", {})
    right_paddle_x = int(right_paddle.get("x", 0))
    right_paddle_y = int(right_paddle.get("y", 0))
    right_paddle_width = right_paddle.get("width", 0)
    right_paddle_height = right_paddle.get("height", 0)

    # Ball
    ball = state.get("ball", {})
    ball_x = int(ball.get("x", 0))
    ball_y = int(ball.get("y", 0))

    # Scores
    scores = state.get("scores", {})
    left_score = scores.get("left", 0)
    right_score = scores.get("right", 0)

    # Countdown (optional float value)
    countdown_raw = state.get("countdown", None)
    countdown = int(countdown_raw) if countdown_raw is not None else None

    render(ball_x, ball_y, left_paddle_y, right_paddle_y, left_score, right_score, countdown)
    return state

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

def send_key_event(ws, key_name, is_pressed):
    # Prepare and send the key event to the WebSocket server
    data = {
        "type": "key_event",
        "key": key_name,
        "is_pressed": is_pressed
    }
    ws.send(json.dumps(data))
    print(f"Sent key event: {key_name} {'pressed' if is_pressed else 'released'}")

def listen_to_keys(ws):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        while True:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                ch = sys.stdin.read(1)
                key = None
                if ch == '\x1b':
                    if select.select([sys.stdin], [], [], 0.05)[0]:
                        ch += sys.stdin.read(2)  # usually arrow keys produce 3-character sequences
                if ch in ['w', 's']:
                    key = ch
                elif ch == 'i':  # Up arrow
                    key = 'ArrowUp'
                elif ch == 'k':  # Down arrow
                    key = 'ArrowDown'
                
                if key:
                    send_key_event(ws, key, True)
    except Exception as e:
        print("Key listening error:", e)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def connect_websocket(match_id, left_username, right_username):
    ws_url = f"ws://localhost:8000/ws/game/{match_id}"

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

        # Start a thread to listen for key input using our custom reader.
        threading.Thread(target=listen_to_keys, args=(ws,), daemon=True).start()

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