import threading
import time
import asyncio

# Configuración del juego
WIDTH, HEIGHT = 800, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE, PADDLE_SPEED, BALL_SPEED = 20, 6, 3


class GameState:
    def __init__(self):
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = PADDLE_WIDTH, PADDLE_HEIGHT
        self.BALL_SIZE = BALL_SIZE
        self.PADDLE_SPEED = PADDLE_SPEED
        self.BALL_SPEED = BALL_SPEED

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

    def process_key_event(self, key, is_pressed):
        if key == "w":
            self.left_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
        elif key == "s":
            self.left_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0
        elif key == "ArrowUp":
            self.right_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
        elif key == "ArrowDown":
            self.right_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0

    def update(self):
        self._update_paddles()
        self._update_ball()

    def _update_paddles(self):
        for paddle in [self.left_paddle, self.right_paddle]:
            paddle["y"] += paddle["dy"]
            paddle["y"] = max(0, min(self.HEIGHT - self.PADDLE_HEIGHT, paddle["y"]))

    def _update_ball(self):
        self.ball["x"] += self.ball["speedX"]
        self.ball["y"] += self.ball["speedY"]

        # Rebotes
        if self.ball["y"] <= 0 or self.ball["y"] >= self.HEIGHT:
            self.ball["speedY"] *= -1

        # Colisiones con paletas
        if self._check_collision(self.left_paddle) or self._check_collision(
            self.right_paddle
        ):
            self.ball["speedX"] *= -1

        # Reset si la pelota sale
        if self.ball["x"] <= 0 or self.ball["x"] >= self.WIDTH:
            self._reset_ball()

    def _check_collision(self, paddle):
        return (
            paddle["x"] < self.ball["x"] < paddle["x"] + self.PADDLE_WIDTH
            and paddle["y"] < self.ball["y"] < paddle["y"] + self.PADDLE_HEIGHT
        )

    def _reset_ball(self):
        self.ball["x"] = self.WIDTH // 2
        self.ball["y"] = self.HEIGHT // 2
        self.ball["speedX"] *= -1

    def get_state(self):
        return {
            "left_paddle": self.left_paddle,
            "right_paddle": self.right_paddle,
            "ball": self.ball,
        }
