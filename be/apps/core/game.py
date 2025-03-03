import requests
import time
import math
import threading

API_URL = "http://localhost:8000/api/history/match/"

class GameState:
    def __init__(self, match_id=None):
        self.WIDTH, self.HEIGHT = 800, 400
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 20, 100
        self.BALL_SIZE = 35
        self.PADDLE_SPEED = 8
        self.BALL_SPEED = 8
        self.MAX_BALL_SPEED = 16
        self.BALL_ACCELERATION = 1.05
        self.MIN_BOUNCE_ANGLE = math.pi / 12  # Ángulo mínimo de rebote (15 grados)
        self.MAX_BOUNCE_ANGLE = math.pi / 3   # Ángulo máximo de rebote (60 grados)
        self.running = False
        self.last_update = time.time()
        self.fps_cap = 60

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
            "radius": self.BALL_SIZE // 2,
            "speedX": self.BALL_SPEED,
            "speedY": self.BALL_SPEED / 2,
            "last_hit": None,
        }

        self.scores = {"left": 0, "right": 0}
        self.match_id = match_id
        self.game_over = False

    def start_game(self, match_id):
        """Inicia el juego con un ID de partido"""
        if match_id:
            self.match_id = match_id
            print(f"✅ Match ID asignado: {self.match_id}")
        else:
            print("⚠️ No se proporcionó un match_id válido.")

        self.running = True
        self.game_over = False
        self.scores = {"left": 0, "right": 0}
        self.reset_ball()

    def reset_ball(self):
        """Reinicia la pelota en el centro con dirección aleatoria"""
        direction = -1 if self.ball.get("last_hit") == "right" else 1
        
        # Si es el primer lanzamiento o después de un gol, alterna la dirección
        if not hasattr(self, '_last_scorer'):
            self._last_scorer = "left"
        else:
            direction = -1 if self._last_scorer == "left" else 1
        
        # Velocidad inicial predecible pero con ligera variación en Y
        self.ball = {
            "x": self.WIDTH // 2,
            "y": self.HEIGHT // 2,
            "radius": self.BALL_SIZE // 2,
            "speedX": self.BALL_SPEED * direction,
            "speedY": self.BALL_SPEED / 2 * (0.5 if direction > 0 else -0.5),
            "last_hit": None,
        }

    def update(self):
        """Actualiza el estado del juego"""
        # Control de tiempo delta para física consistente
        current_time = time.time()
        dt = min(current_time - self.last_update, 1/30)  # Limita dt para evitar saltos grandes
        self.last_update = current_time

        # Factor de escala de tiempo para mantener velocidad constante
        time_factor = dt * self.fps_cap

        self._update_paddles(time_factor)
        if self.running and not self.game_over:
            self._update_ball(time_factor)

    def _update_paddles(self, time_factor):
        """Mueve las paletas dentro de los límites"""
        for paddle in [self.left_paddle, self.right_paddle]:
            # Movimiento suave basado en delta time
            paddle["y"] += paddle["dy"] * time_factor
            # Restricción de bordes mejorada
            paddle["y"] = max(0, min(self.HEIGHT - paddle["height"], paddle["y"]))

    def _calculate_paddle_bounce(self, hit_paddle, ball_y, speed):
        """Calcula el rebote mejorado con la paleta basado en la posición de impacto"""
        # Calcula la posición relativa del impacto en la paleta (0 = centro, -1 = extremo superior, 1 = extremo inferior)
        paddle_center = hit_paddle["y"] + hit_paddle["height"] / 2
        paddle_half_height = hit_paddle["height"] / 2
        
        # Normaliza la posición entre -1 y 1
        relative_position = (ball_y - paddle_center) / paddle_half_height
        
        # Limita la posición relativa entre -0.95 y 0.95 para evitar ángulos demasiado extremos
        relative_position = max(min(relative_position, 0.95), -0.95)
        
        # Aumenta ligeramente el efecto del extremo para rebotes más variados
        # Esto hace que los rebotes cerca de los extremos sean más pronunciados
        relative_position = math.copysign(math.pow(abs(relative_position), 0.8), relative_position)
        
        # Calcula el ángulo de rebote basado en la posición relativa, entre MIN_BOUNCE_ANGLE y MAX_BOUNCE_ANGLE
        bounce_angle = relative_position * self.MAX_BOUNCE_ANGLE
        
        # Determina la dirección del rebote según qué paleta fue golpeada
        direction = 1 if hit_paddle == self.left_paddle else -1
        
        # Aplica un pequeño incremento de velocidad para hacer el juego más dinámico
        speed = min(speed * self.BALL_ACCELERATION, self.MAX_BALL_SPEED)
        
        # Calcula las nuevas componentes de velocidad
        speed_x = math.cos(bounce_angle) * direction * speed
        speed_y = math.sin(bounce_angle) * speed
        
        # Asegura una velocidad mínima en X para evitar rebotes horizontales muy lentos
        min_speed_x = speed * 0.5
        if abs(speed_x) < min_speed_x:
            speed_x = math.copysign(min_speed_x, speed_x)
        
        return speed_x, speed_y

    def _update_ball(self, time_factor):
        """Mueve la pelota y detecta colisiones con física mejorada"""
        if self.scores["left"] >= 5 or self.scores["right"] >= 5:
            print("🏁 El juego ha terminado.")
            self.running = False
            self.game_over = True
            return

        # Actualiza posición basada en velocidad y delta time
        next_x = self.ball["x"] + self.ball["speedX"] * time_factor
        next_y = self.ball["y"] + self.ball["speedY"] * time_factor

        # Colisión con paredes (techo y suelo)
        if next_y - self.ball["radius"] <= 0:
            # Rebote en el techo
            self.ball["speedY"] = abs(self.ball["speedY"])
            next_y = self.ball["radius"]  # Corrige posición para evitar "pegarse" al borde
        elif next_y + self.ball["radius"] >= self.HEIGHT:
            # Rebote en el suelo
            self.ball["speedY"] = -abs(self.ball["speedY"])
            next_y = self.HEIGHT - self.ball["radius"]  # Corrige posición

        # Verifica colisiones con paletas antes de actualizar posición final
        hit_paddle = None
        
        # Colisión con paleta izquierda
        if (next_x - self.ball["radius"] <= self.left_paddle["x"] + self.left_paddle["width"] and
            self.ball["x"] - self.ball["radius"] > self.left_paddle["x"] + self.left_paddle["width"] and
            next_y + self.ball["radius"] >= self.left_paddle["y"] and
            next_y - self.ball["radius"] <= self.left_paddle["y"] + self.left_paddle["height"]):
            hit_paddle = self.left_paddle
            self.ball["last_hit"] = "left"
            # Ajusta x para evitar atravesar la paleta
            next_x = hit_paddle["x"] + hit_paddle["width"] + self.ball["radius"]
        
        # Colisión con paleta derecha
        elif (next_x + self.ball["radius"] >= self.right_paddle["x"] and
              self.ball["x"] + self.ball["radius"] < self.right_paddle["x"] and
              next_y + self.ball["radius"] >= self.right_paddle["y"] and
              next_y - self.ball["radius"] <= self.right_paddle["y"] + self.right_paddle["height"]):
            hit_paddle = self.right_paddle
            self.ball["last_hit"] = "right"
            # Ajusta x para evitar atravesar la paleta
            next_x = hit_paddle["x"] - self.ball["radius"]
        
        # Procesa rebote realista si golpeó una paleta
        if hit_paddle:
            # Calcula la velocidad actual
            current_speed = math.sqrt(self.ball["speedX"]**2 + self.ball["speedY"]**2)
            
            # Usa la nueva función de rebote mejorada
            speed_x, speed_y = self._calculate_paddle_bounce(hit_paddle, next_y, current_speed)
            
            # Aplica las nuevas velocidades
            self.ball["speedX"] = speed_x
            self.ball["speedY"] = speed_y
            
            # Añade pequeña variación para evitar patrones predecibles en rebotes repetidos
            if abs(self.ball["speedY"]) < current_speed * 0.2:
                # Si la velocidad vertical es muy baja, añade un poco de variación
                variation = current_speed * 0.1 * (-1 if self.ball["speedY"] < 0 else 1)
                self.ball["speedY"] += variation

        # Verifica si hubo gol (después de verificar colisiones con paletas)
        if next_x - self.ball["radius"] <= 0:
            # Gol del jugador derecho
            self._last_scorer = "right"
            self.scores["right"] += 1
            print(f"⚽ Gol del jugador de la derecha - Puntuación: {self.scores['left']} - {self.scores['right']}")
            if self.scores["right"] <= 5:
                threading.Thread(target=self._send_score_update, args=(False,), daemon=True).start()
            self.reset_ball()
            return  # Evita actualizar la posición después de resetear
        elif next_x + self.ball["radius"] >= self.WIDTH:
            # Gol del jugador izquierdo
            self._last_scorer = "left"
            self.scores["left"] += 1
            print(f"⚽ Gol del jugador de la izquierda - Puntuación: {self.scores['left']} - {self.scores['right']}")
            if self.scores["left"] <= 5:
                threading.Thread(target=self._send_score_update, args=(True,), daemon=True).start()
            self.reset_ball()
            return  # Evita actualizar la posición después de resetear
        
        # Actualiza la posición final de la pelota
        self.ball["x"] = next_x
        self.ball["y"] = next_y

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

    def get_state(self):
        """Devuelve el estado actual del juego"""
        return {
            "left_paddle": self.left_paddle,
            "right_paddle": self.right_paddle,
            "ball": self.ball,
            "scores": self.scores,
            "game_over": self.game_over
        }