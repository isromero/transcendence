import requests
import time
import math
import threading  # 👈 Para ejecutar la actualización en un hilo separado

API_URL = "http://localhost:8000/api/history/match/"

class GameState:
    def __init__(self, match_id=None):
        self.WIDTH, self.HEIGHT = 800, 400
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 20, 100
        self.BALL_SIZE = 20
        self.PADDLE_SPEED = 8
        self.BALL_SPEED = 6
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

        self.scores = {"left": 0, "right": 0}
        self.match_id = match_id

    def start_game(self, match_id):
        """Inicia el juego con un ID de partido"""
        if match_id:
            self.match_id = match_id
            print(f"✅ Match ID asignado: {self.match_id}")
        else:
            print("⚠️ No se proporcionó un match_id válido.") 

        self.running = True
        self.scores = {"left": 0, "right": 0}
        self.reset_ball()

    def reset_ball(self):
        """Reinicia la pelota en el centro"""
        self.ball = {
            "x": self.WIDTH // 2,
            "y": self.HEIGHT // 2,
            "radius": self.BALL_SIZE,
            "speedX": self.BALL_SPEED * (-1 if self.ball["speedX"] > 0 else 1),
            "speedY": self.BALL_SPEED,
        }

    def update(self):
        """Actualiza el estado del juego"""
        current_time = time.time()
        dt = current_time - self.last_update
        self.last_update = current_time

        self._update_paddles()
        if self.running:
            self._update_ball(dt)

    def _update_paddles(self):
        """Mueve las paletas dentro de los límites"""
        for paddle in [self.left_paddle, self.right_paddle]:
            paddle["y"] += paddle["dy"]
            paddle["y"] = max(0, min(self.HEIGHT - paddle["height"], paddle["y"]))

    def _update_ball(self, dt):
        """Mueve la pelota y detecta colisiones"""
        if self.scores["left"] >= 5 or self.scores["right"] >= 5:
            print("🏁 El juego ha terminado.")
            self.running = False  # ✅ Detener el juego
            return

        self.ball["x"] += self.ball["speedX"] * dt * 60
        self.ball["y"] += self.ball["speedY"] * dt * 60

        # Colisión con paredes
        if self.ball["y"] - self.ball["radius"] <= 0 or self.ball["y"] + self.ball["radius"] >= self.HEIGHT:
            self.ball["speedY"] *= -1

        # Colisión con paletas
        for paddle in [self.left_paddle, self.right_paddle]:
            if self._check_paddle_collision(paddle):
                self.ball["speedX"] *= -1.1

        # Gol en la portería izquierda (punto para el jugador derecho)
        if self.ball["x"] <= 0:
            self.scores["right"] += 1
            print(f"⚽ Gol del jugador de la derecha - Puntuación: {self.scores['left']} - {self.scores['right']}")
            if self.scores["right"] <= 5:  # ✅ Solo enviar si el juego sigue en curso
                threading.Thread(target=self._send_score_update, args=(False,), daemon=True).start()
            self.reset_ball()

        # Gol en la portería derecha (punto para el jugador izquierdo)
        elif self.ball["x"] >= self.WIDTH:
            self.scores["left"] += 1
            print(f"⚽ Gol del jugador de la izquierda - Puntuación: {self.scores['left']} - {self.scores['right']}")
            if self.scores["left"] <= 5:  # ✅ Solo enviar si el juego sigue en curso
                threading.Thread(target=self._send_score_update, args=(True,), daemon=True).start()
            self.reset_ball()

            
    def process_key_event(self, key, is_pressed):
        """Maneja los eventos de teclado para mover las paletas"""
        if key == "w":
            self.left_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
        elif key == "s":
            self.left_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0
        elif key == "ArrowUp":
            self.right_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
        elif key == "ArrowDown":
            self.right_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0


    def _send_score_update(self, is_player1):
        """Envía la puntuación a la API en un hilo separado"""
        if not self.match_id:
            print("⚠️ No hay match_id, no se puede enviar el puntaje.")
            return

        payload = {"is_player1": is_player1}
        url = f"{API_URL}{self.match_id}"
        headers = {"Content-Type": "application/json"}

        print(f"📡 Enviando PUT a {url} con datos: {payload}")

        try:
            response = requests.put(url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()

            print(f"✅ Puntaje actualizado correctamente: {response.json()}")
        except requests.exceptions.Timeout:
            print("⏳ La solicitud de actualización de puntuación tardó demasiado. Reintentando en la próxima actualización...")
        except requests.exceptions.ConnectionError:
            print("❌ No se pudo conectar con la API. Verifica que el servidor está en ejecución.")
        except requests.exceptions.HTTPError as e:
            print(f"⚠️ Error HTTP al actualizar puntaje: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error inesperado al actualizar puntaje: {e}")

    def _check_paddle_collision(self, paddle):
        """Verifica si la pelota choca con una paleta"""
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
        """Devuelve el estado actual del juego"""
        return {
            "left_paddle": self.left_paddle,
            "right_paddle": self.right_paddle,
            "ball": self.ball,
            "scores": self.scores,
        }
