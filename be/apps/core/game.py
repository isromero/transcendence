import threading
import time

# Configuración del juego
WIDTH, HEIGHT = 800, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE, PADDLE_SPEED, BALL_SPEED = 20, 6, 3

left_paddle = {"x": 30, "y": HEIGHT // 2 - PADDLE_HEIGHT // 2, "dy": 0, "width": PADDLE_WIDTH, "height": PADDLE_HEIGHT}
right_paddle = {"x": WIDTH - 30 - PADDLE_WIDTH, "y": HEIGHT // 2 - PADDLE_HEIGHT // 2, "dy": 0, "width": PADDLE_WIDTH, "height": PADDLE_HEIGHT}
ball = {"x": WIDTH // 2, "y": HEIGHT // 2, "radius": BALL_SIZE, "speedX": BALL_SPEED, "speedY": BALL_SPEED}

def update_game():
    while True:
        move_paddles()
        move_ball()
        time.sleep(1 / 60)

def move_paddles():
    left_paddle["y"] += left_paddle["dy"]
    right_paddle["y"] += right_paddle["dy"]

    left_paddle["y"] = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle["y"]))
    right_paddle["y"] = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle["y"]))

def move_ball():
    ball["x"] += ball["speedX"]
    ball["y"] += ball["speedY"]

    if ball["y"] - BALL_SIZE <= 0 or ball["y"] + BALL_SIZE >= HEIGHT:
        ball["speedY"] *= -1

    if check_collision(left_paddle) or check_collision(right_paddle):
        ball["speedX"] *= -1

    if ball["x"] - BALL_SIZE <= 0 or ball["x"] + BALL_SIZE >= WIDTH:
        ball["x"], ball["y"] = WIDTH // 2, HEIGHT // 2
        ball["speedX"], ball["speedY"] = BALL_SPEED * (-1 if ball["speedX"] > 0 else 1), BALL_SPEED

def check_collision(paddle):
    return (
        paddle["x"] < ball["x"] < paddle["x"] + PADDLE_WIDTH and
        paddle["y"] < ball["y"] < paddle["y"] + PADDLE_HEIGHT
    )

def process_key_event(key, is_pressed):
    if key == "w":
        left_paddle["dy"] = -PADDLE_SPEED if is_pressed else 0
    elif key == "s":
        left_paddle["dy"] = PADDLE_SPEED if is_pressed else 0
    elif key == "ArrowUp":
        right_paddle["dy"] = -PADDLE_SPEED if is_pressed else 0
    elif key == "ArrowDown":
        right_paddle["dy"] = PADDLE_SPEED if is_pressed else 0

def update_paddles():
    """ Lógica para actualizar las posiciones de las paletas """
    global left_paddle, right_paddle
    left_paddle['y'] += left_paddle['dy']
    right_paddle['y'] += right_paddle['dy']

    # Evitar que las paletas salgan del área de juego
    left_paddle['y'] = max(0, min(left_paddle['y'], 400 - left_paddle['height']))
    right_paddle['y'] = max(0, min(right_paddle['y'], 400 - right_paddle['height']))

def update_ball():
    """ Lógica para actualizar la posición de la pelota """
    global ball
    ball['x'] += ball['speedX']
    ball['y'] += ball['speedY']

    # Rebote en las paredes superior e inferior
    if ball['y'] <= 0 or ball['y'] >= 400:
        ball['speedY'] *= -1


def game_loop():
    """ Bucle infinito para actualizar el juego """
    while True:
        update_paddles()
        update_ball()
        time.sleep(0.016)  # ~60 FPS (1s / 60 = 0.016s)

# Iniciar el hilo del juego
threading.Thread(target=game_loop, daemon=True).start()
game_thread = threading.Thread(target=update_game, daemon=True)
game_thread.start()
