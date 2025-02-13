# Configuración del juego
WIDTH = 800
HEIGHT = 400
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SIZE = 20
PADDLE_SPEED = 6
BALL_SPEED = 3

# Inicializar posiciones
left_paddle = {"x": 30, "y": HEIGHT // 2 - PADDLE_HEIGHT // 2, "dy": 0}
right_paddle = {"x": WIDTH - 30 - PADDLE_WIDTH, "y": HEIGHT // 2 - PADDLE_HEIGHT // 2, "dy": 0}
ball = {"x": WIDTH // 2, "y": HEIGHT // 2, "speedX": BALL_SPEED, "speedY": BALL_SPEED}

def update_paddles():
    """ Mueve las paletas dentro de los límites del campo """
    left_paddle["y"] += left_paddle["dy"]
    right_paddle["y"] += right_paddle["dy"]

    # Limitar las paletas dentro del área de juego
    left_paddle["y"] = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle["y"]))
    right_paddle["y"] = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle["y"]))

def update_ball():
    """ Mueve la pelota y detecta colisiones """
    ball["x"] += ball["speedX"]
    ball["y"] += ball["speedY"]

    # Rebote con bordes superior e inferior
    if ball["y"] - BALL_SIZE <= 0 or ball["y"] + BALL_SIZE >= HEIGHT:
        ball["speedY"] = -ball["speedY"]

    # Comprobación de colisión con las paletas
    def check_paddle_collision(paddle):
        if (
            ball["x"] - BALL_SIZE <= paddle["x"] + PADDLE_WIDTH
            and ball["x"] + BALL_SIZE >= paddle["x"]
            and ball["y"] >= paddle["y"]
            and ball["y"] <= paddle["y"] + PADDLE_HEIGHT
        ):
            relativeIntersectY = (ball["y"] - (paddle["y"] + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2)
            bounceAngle = relativeIntersectY * (3.14 / 4)  # Ángulo de rebote máximo 45°

            # Mantener la velocidad constante pero cambiar la dirección
            speed = (ball["speedX"] ** 2 + ball["speedY"] ** 2) ** 0.5
            ball["speedX"] = (-1 if paddle == right_paddle else 1) * abs(speed) * 1.1
            ball["speedY"] = speed * relativeIntersectY * 1.1

    check_paddle_collision(left_paddle)
    check_paddle_collision(right_paddle)

    # Reiniciar la pelota si sale de los límites
    if ball["x"] - BALL_SIZE <= 0 or ball["x"] + BALL_SIZE >= WIDTH:
        ball["x"], ball["y"] = WIDTH // 2, HEIGHT // 2
        ball["speedX"], ball["speedY"] = BALL_SPEED * (-1 if ball["speedX"] > 0 else 1), BALL_SPEED

def process_key_event(key, is_pressed):
    """ Recibe eventos de teclado y actualiza la dirección de las paletas """
    if key == "w":
        left_paddle["dy"] = -PADDLE_SPEED if is_pressed else 0
    elif key == "s":
        left_paddle["dy"] = PADDLE_SPEED if is_pressed else 0
    elif key == "ArrowUp":
        right_paddle["dy"] = -PADDLE_SPEED if is_pressed else 0
    elif key == "ArrowDown":
        right_paddle["dy"] = PADDLE_SPEED if is_pressed else 0
