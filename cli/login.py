import os
import requests
import websocket
import json
import time

# Game and ASCII canvas settings (assumed game size: 800x400, ASCII: 80x40)
GAME_WIDTH = 800
GAME_HEIGHT = 400
ASCII_WIDTH = 80
ASCII_HEIGHT = 40
SCALE_X = ASCII_WIDTH / GAME_WIDTH  # 0.1
SCALE_Y = ASCII_HEIGHT / GAME_HEIGHT  # 0.1

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_game(state):
    """
    Render the game state in an ASCII canvas.
    Expected state keys: left_paddle, right_paddle, ball, scores, countdown.
    """
    # Create an empty canvas (2D list of spaces)
    canvas = [[' ' for _ in range(ASCII_WIDTH)] for _ in range(ASCII_HEIGHT)]
    
    # Extract game objects
    left_paddle = state.get("left_paddle", {})
    right_paddle = state.get("right_paddle", {})
    ball = state.get("ball", {})
    scores = state.get("scores", {"left": 0, "right": 0})
    countdown = state.get("countdown", None)
    
    # Draw left paddle (using '|')
    lp_x = int(left_paddle.get("x", 0) * SCALE_X)
    lp_y = int(left_paddle.get("y", 0) * SCALE_Y)
    lp_w = max(1, int(left_paddle.get("width", 0) * SCALE_X))
    lp_h = max(1, int(left_paddle.get("height", 0) * SCALE_Y))
    for i in range(lp_y, min(lp_y + lp_h, ASCII_HEIGHT)):
        for j in range(lp_x, min(lp_x + lp_w, ASCII_WIDTH)):
            canvas[i][j] = '|'
    
    # Draw right paddle (using '|')
    rp_x = int(right_paddle.get("x", 0) * SCALE_X)
    rp_y = int(right_paddle.get("y", 0) * SCALE_Y)
    rp_w = max(1, int(right_paddle.get("width", 0) * SCALE_X))
    rp_h = max(1, int(right_paddle.get("height", 0) * SCALE_Y))
    for i in range(rp_y, min(rp_y + rp_h, ASCII_HEIGHT)):
        for j in range(rp_x, min(rp_x + rp_w, ASCII_WIDTH)):
            canvas[i][j] = '|'
    
    # Draw the ball (using 'O')
    ball_x = int(ball.get("x", 0) * SCALE_X)
    ball_y = int(ball.get("y", 0) * SCALE_Y)
    if 0 <= ball_y < ASCII_HEIGHT and 0 <= ball_x < ASCII_WIDTH:
        canvas[ball_y][ball_x] = 'O'
        
    # Build a string representation of the canvas
    rendered_canvas = "\n".join("".join(row) for row in canvas)
    
    # Build header (display scores and countdown)
    header = f"Score: Left {scores.get('left', 0)} - Right {scores.get('right', 0)}\n"
    if countdown is not None:
        header += f"Countdown: {countdown:.2f}\n"
    else:
        header += "Countdown: --\n"
    
    return header + rendered_canvas

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

def connect_websocket(match_id):
    ws_url = f"ws://localhost:8000/ws/game/{match_id}"  # Adjust hostname if needed
    
    def on_message(ws, message):
        try:
            state = json.loads(message)
        except Exception as e:
            print("Could not parse message as JSON:", message)
            return
        
        # Clear console and render ASCII art
        clear_console()
        rendered = render_game(state)
        print(rendered)
    
    def on_error(ws, error):
        print("WebSocket Error:", error)
    
    def on_close(ws, close_status_code, close_msg):
        print("WebSocket closed")
    
    def on_open(ws):
        print("WebSocket connection opened")
    
    # Explicitly import WebSocketApp from the websocket module
    from websocket import WebSocketApp
    ws_app = WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws_app.on_open = on_open
    ws_app.run_forever()


# Example usage
api_url = "http://localhost:8000/api/"  # Replace with your API URL
username = "testotest"
password = "test1234test!A"
session, message, cookies = login_and_get_cookie(api_url, username, password)

if session:
    match_data = create_match(api_url, session)
    if match_data and "data" in match_data:
        match_id = match_data["data"].get("match_id")
        if match_id:
            connect_websocket(match_id)