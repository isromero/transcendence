import threading
import time
import asyncio
import math
import copy
import requests

# Configuración del juego
WIDTH, HEIGHT = 800, 400
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE, PADDLE_SPEED, BALL_SPEED = 20, 8, 6

API_URL = "http://localhost:8000/api/history/match/"

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

        self.scores = {"left": 0, "right": 0}  # Puntuaciones de los jugadores
        self.match_id = None  # ID del partido
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

    def start_game(self, match_id):
        self.running = True
        self.match_id = match_id  # Guardar el ID del partido
        self.scores = {"left": 0, "right": 0}  # Reiniciar puntajes
        self.reset_ball()

    def reset_ball(self):
        self.ball = {
            "x": self.WIDTH // 2,
            "y": self.HEIGHT // 2,
            "radius": self.BALL_SIZE,
            "speedX": self.BALL_SPEED * (-1 if self.ball["speedX"] > 0 else 1),
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
            self.ball["y"] = self.ball["radius"]
            self.ball["speedY"] *= -1

        elif self.ball["y"] + self.ball["radius"] >= self.HEIGHT:
            self.ball["y"] = self.HEIGHT - self.ball["radius"]
            self.ball["speedY"] *= -1

        # Colisión con paletas
        for paddle in [self.left_paddle, self.right_paddle]:
            if self._check_paddle_collision(paddle):
                self.ball["speedX"] *= -1.1

        # Verificar si la pelota salió del campo
        if self.ball["x"] <= 0:
            self.scores["right"] += 1  # Punto para el jugador de la derecha
            self._send_score_update(False)  # Player 1 es False (derecha)
            
            if self.scores["right"] >= 50000:  # Fin del juego si llega a 5 puntos
                self._end_game(winner="right")
                return

            self.reset_ball()

        elif self.ball["x"] >= self.WIDTH:
            self.scores["left"] += 1  # Punto para el jugador de la izquierda
            self._send_score_update(True)  # Player 1 es True (izquierda)

            if self.scores["left"] >= 50000:  # Fin del juego si llega a 5 puntos
                self._end_game(winner="left")
                return

            self.reset_ball()

        #print(f"Puntaje: {self.scores}")


    def _send_score_update(self, player1):
        """Envía una solicitud PUT al servidor cuando se anota un punto."""
        if not self.match_id:
            return
        
        payload = {
            "player1": player1,
            "score": 1  # Se suma un punto al jugador correspondiente
        }

        try:
            url = f"{API_URL}{self.match_id}"
            response = requests.put(url, json=payload)

            if response.status_code == 200:
                print(f"Punto registrado correctamente para {'izquierda' if player1 else 'derecha'}.")
            else:
                print(f"Error al actualizar el puntaje: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")

    def _check_paddle_collision(self, paddle):
        next_x = self.ball["x"] + self.ball["speedX"]
        next_y = self.ball["y"] + self.ball["speedY"]

        if (
            next_x - self.ball["radius"] <= paddle["x"] + paddle["width"]
            and next_x + self.ball["radius"] >= paddle["x"]
            and next_y + self.ball["radius"] >= paddle["y"]
            and next_y - self.ball["radius"] <= paddle["y"] + paddle["height"]
        ):
            relative_intersect_y = (self.ball["y"] - (paddle["y"] + paddle["height"] / 2)) / (paddle["height"] / 2)
            bounce_angle = relative_intersect_y * (math.pi / 4)

            speed = math.sqrt(self.ball["speedX"] ** 2 + self.ball["speedY"] ** 2)
            direction = -1 if self.ball["x"] < self.WIDTH // 2 else 1

            self.ball["speedX"] = math.cos(bounce_angle) * direction * speed
            self.ball["speedY"] = math.sin(bounce_angle) * speed

            return True

        return False

    def get_state(self):
        return {
            "left_paddle": self.left_paddle,
            "right_paddle": self.right_paddle,
            "ball": self.ball,
            "scores": self.scores,
        }
    
    def _end_game(self, winner):
        """Finaliza el juego y envía la actualización final al servidor."""
        print(f"¡Juego terminado! Ganador: {winner}")
        self.running = False  # Detener la actualización del juego
        
        # Enviar resultado final al servidor
        if self.match_id:
            payload = {
                "match_id": self.match_id,
                "winner": winner
            }
            try:
                url = f"{API_URL}{self.match_id}/end"
                response = requests.put(url, json=payload)

                if response.status_code == 200:
                    print(f"Resultado final registrado: Ganador -> {winner}.")
                else:
                    print(f"Error al registrar el resultado final: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Error al conectar con la API: {e}")

