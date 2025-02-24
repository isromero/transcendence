import threading
import time
import asyncio
import math
import copy

# Configuración del juego
WIDTH, HEIGHT = 800, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE, PADDLE_SPEED, BALL_SPEED = 20, 8, 6


class GameState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameState, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = PADDLE_WIDTH, PADDLE_HEIGHT
        self.BALL_SIZE = BALL_SIZE
        self.PADDLE_SPEED = PADDLE_SPEED
        self.BALL_SPEED = BALL_SPEED
        self.running = False
        self.last_update = time.time()

        self.left_paddle = {
            "x": 30,
            "y": self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2,
            "dy": 0,
            "width": self.PADDLE_WIDTH,
            "height": self.PADDLE_HEIGHT,
        }

        self.right_paddle = {
            "x": self.WIDTH - 30 - self.PADDLE_WIDTH,
            "y": self.HEIGHT // 2 - self.PADDLE_HEIGHT // 2,
            "dy": 0,
            "width": self.PADDLE_WIDTH,
            "height": self.PADDLE_HEIGHT,
        }

        self.ball = {
            "x": self.WIDTH // 2,
            "y": self.HEIGHT // 2,
            "radius": self.BALL_SIZE,
            "speedX": self.BALL_SPEED,
            "speedY": self.BALL_SPEED,
        }

        self._initialized = True

    def process_key_event(self, key, is_pressed):
        if key == "w":
            self.left_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
        elif key == "s":
            self.left_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0
        elif key == "ArrowUp":
            self.right_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
        elif key == "ArrowDown":
            self.right_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0

    def start_game(self):
        self.running = True
        self.ball = {
            "x": self.WIDTH // 2,
            "y": self.HEIGHT // 2,
            "radius": self.BALL_SIZE,
            "speedX": self.BALL_SPEED,
            "speedY": self.BALL_SPEED,
        }

    def update(self):
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time

        self._update_paddles()
        if self.running:
            self._update_ball(dt)

    def _update_paddles(self):
        for paddle in [self.left_paddle, self.right_paddle]:
            paddle["y"] += paddle["dy"]
            paddle["y"] = max(0, min(self.HEIGHT - paddle["height"], paddle["y"]))

    def _update_ball(self, dt):
        # Actualizar posición de la pelota
        self.ball["x"] += self.ball["speedX"] * dt * 60
        self.ball["y"] += self.ball["speedY"] * dt * 60

            # Colisión con paredes superior e inferior
        if self.ball["y"] - self.ball["radius"] <= 0:
            self.ball["y"] = self.ball["radius"]  # Asegurar que la pelota no atraviese el borde
            self.ball["speedY"] *= -1  # Invertir dirección

        elif self.ball["y"] + self.ball["radius"] >= self.HEIGHT:
            self.ball["y"] = self.HEIGHT - self.ball["radius"]  # Ajustar posición
            self.ball["speedY"] *= -1  # Invertir dirección


        # Colisión con paletas
        for paddle in [self.left_paddle, self.right_paddle]:
            if self._check_paddle_collision(paddle):
                self.ball["speedX"] *= -1.1  # Aumentar velocidad ligeramente

        # Verificar si la pelota salió del campo
        if self.ball["x"] <= 0 or self.ball["x"] >= self.WIDTH:
            self.ball["x"] = self.WIDTH // 2
            self.ball["y"] = self.HEIGHT // 2
            self.ball["speedX"] = self.BALL_SPEED * (-1 if self.ball["x"] <= 0 else 1)
            self.ball["speedY"] = self.BALL_SPEED

    def _check_paddle_collision(self, paddle):
        next_x = self.ball["x"] + self.ball["speedX"]  # Predecir la siguiente posición X
        next_y = self.ball["y"] + self.ball["speedY"]  # Predecir la siguiente posición Y

        # Verificar si la pelota va a chocar en el siguiente frame
        if (
            next_x - self.ball["radius"] <= paddle["x"] + paddle["width"]
            and next_x + self.ball["radius"] >= paddle["x"]
            and next_y + self.ball["radius"] >= paddle["y"]
            and next_y - self.ball["radius"] <= paddle["y"] + paddle["height"]
        ):
            # Calcular el ángulo de rebote según el punto de impacto
            relative_intersect_y = (self.ball["y"] - (paddle["y"] + paddle["height"] / 2)) / (paddle["height"] / 2)
            bounce_angle = relative_intersect_y * (math.pi / 4)  # Máximo 45 grados

            # Mantener la velocidad constante pero ajustando dirección
            speed = math.sqrt(self.ball["speedX"] ** 2 + self.ball["speedY"] ** 2)  # Mantiene la velocidad actual
            direction = -1 if self.ball["x"] < self.WIDTH // 2 else 1

            # Aplicar el rebote sin recolocar la pelota
            self.ball["speedX"] = math.cos(bounce_angle) * direction * speed
            self.ball["speedY"] = math.sin(bounce_angle) * speed

            return True

        return False



    def get_state(self):
        state = {
            "left_paddle": {
                "x": round(self.left_paddle["x"]),
                "y": round(self.left_paddle["y"]),
                "dy": self.left_paddle["dy"],
                "width": self.left_paddle["width"],
                "height": self.left_paddle["height"],
            },
            "right_paddle": {
                "x": round(self.right_paddle["x"]),
                "y": round(self.right_paddle["y"]),
                "dy": self.right_paddle["dy"],
                "width": self.right_paddle["width"],
                "height": self.right_paddle["height"],
            },
            "ball": {
                "x": round(self.ball["x"]),
                "y": round(self.ball["y"]),
                "radius": self.ball["radius"],
                "speedX": round(self.ball["speedX"], 2),
                "speedY": round(self.ball["speedY"], 2),
            },
        }
        return state
