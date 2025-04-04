import requests
import time
import math
from channels.db import database_sync_to_async


class GameState:
    def __init__(self, match_id=None):
        self.WIDTH, self.HEIGHT = 800, 400
        self.PADDLE_WIDTH, self.PADDLE_HEIGHT = 20, 100
        self.BALL_SIZE = 35
        self.PADDLE_SPEED = 7
        self.BALL_SPEED = 4
        self.MAX_BALL_SPEED = 16
        self.BALL_ACCELERATION = 1.05
        self.MIN_BOUNCE_ANGLE = math.pi / 12  # Minimum bounce angle (15 degrees)
        self.MAX_BOUNCE_ANGLE = math.pi / 3  # Maximum bounce angle (60 degrees)
        self.running = False
        self.last_update = time.time()
        self.fps_cap = 90
        self.countdown = 0  # Countdown timer in seconds

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
        """Init game with a match id"""
        if match_id:
            self.match_id = match_id
        else:
            raise ValueError("Match ID is required")

        self.running = True
        self.game_over = False
        self.scores = {"left": 0, "right": 0}
        self.reset_ball()
        self.countdown = 5  # Set a 5-second countdown when starting the game

    def reset_ball(self):
        """Reset ball to the center"""
        direction = -1 if self.ball.get("last_hit") == "right" else 1

        # If it's the first launch or after a goal, alternate the direction
        if not hasattr(self, "_last_scorer"):
            self._last_scorer = "left"
        else:
            direction = -1 if self._last_scorer == "left" else 1

        # Predictable initial speed but with slight variation in Y
        """Reset ball to the center"""
        self.ball = {
            "x": self.WIDTH // 2,
            "y": self.HEIGHT // 2,
            "radius": self.BALL_SIZE // 2,
            "speedX": self.BALL_SPEED * direction,
            "speedY": self.BALL_SPEED / 2 * (0.5 if direction > 0 else -0.5),
            "last_hit": None,
        }

    async def update(self):
        """Update game state"""
        current_time = time.time()
        dt = min(current_time - self.last_update, 1 / 30)
        self.last_update = current_time

        if self.countdown > 0:
            self.countdown -= dt
            if self.countdown < 0:
                self.countdown = 0

        self._update_paddles(dt * self.fps_cap)

        if self.running and not self.game_over and self.countdown <= 0:
            await self._update_ball(dt * self.fps_cap)

    def _update_paddles(self, time_factor):
        """Move paddles within the limits"""
        for paddle in [self.left_paddle, self.right_paddle]:
            # Smooth movement based on delta time
            paddle["y"] += paddle["dy"] * time_factor
            # Improved edge restriction
            paddle["y"] = max(0, min(self.HEIGHT - paddle["height"], paddle["y"]))

    def _calculate_paddle_bounce(self, hit_paddle, ball_y, speed):
        """Calculate the improved paddle bounce based on the impact position"""
        # Calculate the relative impact position on the paddle (0 = center, -1 = top edge, 1 = bottom edge)
        paddle_center = hit_paddle["y"] + hit_paddle["height"] / 2
        paddle_half_height = hit_paddle["height"] / 2

        # Normalize the position between -1 and 1
        relative_position = (ball_y - paddle_center) / paddle_half_height

        # Limit the relative position between -0.95 and 0.95 to avoid extreme angles
        relative_position = max(min(relative_position, 0.95), -0.95)

        # Slightly increase the effect of the edge for more varied bounces
        # This makes bounces near the edges more pronounced
        relative_position = math.copysign(
            math.pow(abs(relative_position), 0.8), relative_position
        )

        # Calculate the bounce angle based on the relative position, between MIN_BOUNCE_ANGLE and MAX_BOUNCE_ANGLE
        bounce_angle = relative_position * self.MAX_BOUNCE_ANGLE

        # Determine the direction of the bounce based on which paddle was hit
        direction = 1 if hit_paddle == self.left_paddle else -1

        # Apply a small speed increase to make the game more dynamic
        speed = min(speed * self.BALL_ACCELERATION, self.MAX_BALL_SPEED)

        # Calculate the new speed components
        speed_x = math.cos(bounce_angle) * direction * speed
        speed_y = math.sin(bounce_angle) * speed

        # Ensure a minimum speed in X to avoid very slow horizontal bounces
        min_speed_x = speed * 0.5
        if abs(speed_x) < min_speed_x:
            speed_x = math.copysign(min_speed_x, speed_x)

        return speed_x, speed_y

    async def _update_ball(self, time_factor):
        """Move the ball and detect collisions with improved physics"""
        if self.scores["left"] >= 5 or self.scores["right"] >= 5:
            self.running = False
            self.game_over = True

        # Update position based on speed and delta time
        next_x = self.ball["x"] + self.ball["speedX"] * time_factor
        next_y = self.ball["y"] + self.ball["speedY"] * time_factor

        # Wall collision (ceiling and floor)
        if next_y - self.ball["radius"] <= 0:
            # Bounce on the ceiling
            self.ball["speedY"] = abs(self.ball["speedY"])
            next_y = self.ball[
                "radius"
            ]  # Correct position to avoid sticking to the edge
        elif next_y + self.ball["radius"] >= self.HEIGHT:
            # Bounce on the floor
            self.ball["speedY"] = -abs(self.ball["speedY"])
            next_y = self.HEIGHT - self.ball["radius"]  # Correct position

        # Check paddle collisions before updating final position
        hit_paddle = None

        # Paddle collision (left)
        if (
            next_x - self.ball["radius"]
            <= self.left_paddle["x"] + self.left_paddle["width"]
            and self.ball["x"] - self.ball["radius"]
            > self.left_paddle["x"] + self.left_paddle["width"]
            and next_y + self.ball["radius"] >= self.left_paddle["y"]
            and next_y - self.ball["radius"]
            <= self.left_paddle["y"] + self.left_paddle["height"]
        ):
            hit_paddle = self.left_paddle
            self.ball["last_hit"] = "left"
            # Adjust x to avoid passing through the paddle
            next_x = hit_paddle["x"] + hit_paddle["width"] + self.ball["radius"]

        # Paddle collision (right)
        elif (
            next_x + self.ball["radius"] >= self.right_paddle["x"]
            and self.ball["x"] + self.ball["radius"] < self.right_paddle["x"]
            and next_y + self.ball["radius"] >= self.right_paddle["y"]
            and next_y - self.ball["radius"]
            <= self.right_paddle["y"] + self.right_paddle["height"]
        ):
            hit_paddle = self.right_paddle
            self.ball["last_hit"] = "right"
            # Adjust x to avoid passing through the paddle
            next_x = hit_paddle["x"] - self.ball["radius"]

        # Process realistic bounce if hit a paddle
        if hit_paddle:
            # Calculate current speed
            current_speed = math.sqrt(
                self.ball["speedX"] ** 2 + self.ball["speedY"] ** 2
            )

            # Use the improved bounce function
            speed_x, speed_y = self._calculate_paddle_bounce(
                hit_paddle, next_y, current_speed
            )

            # Apply the new speeds
            self.ball["speedX"] = speed_x
            self.ball["speedY"] = speed_y

            # Add small variation to avoid predictable patterns in repeated bounces
            if abs(self.ball["speedY"]) < current_speed * 0.2:
                # If the vertical speed is very low, add a bit of variation
                variation = current_speed * 0.1 * (-1 if self.ball["speedY"] < 0 else 1)
                self.ball["speedY"] += variation

        # Check if there was a goal (after checking paddle collisions)
        if next_x - self.ball["radius"] <= 0:
            # Right player goal
            self._last_scorer = "right"
            self.scores["right"] += 1
            if self.scores["right"] <= 5:
                await self._send_score_update(is_player1=False)
            self.reset_ball()
            return  # Avoid updating position after resetting
        elif next_x + self.ball["radius"] >= self.WIDTH:
            # Left player goal
            self._last_scorer = "left"
            self.scores["left"] += 1
            if self.scores["left"] <= 5:
                await self._send_score_update(is_player1=True)
            self.reset_ball()
            return  # Avoid updating position after resetting

        # Actualiza la posición final de la pelota
        self.ball["x"] = next_x
        self.ball["y"] = next_y

    def process_key_event(self, key, is_pressed):
        """Handle keyboard events to move paddles"""
        if key == "w" or key == "W":
            self.left_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
        elif key == "s" or key == "S":
            self.left_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0
        elif key == "ArrowUp":
            self.right_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
        elif key == "ArrowDown":
            self.right_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0

    def _check_paddle_collision(self, paddle):
        """Check if the ball collides with a paddle"""
        next_x = self.ball["x"] + self.ball["speedX"]
        next_y = self.ball["y"] + self.ball["speedY"]

        if (
            next_x - self.ball["radius"] <= paddle["x"] + paddle["width"]
            and next_x + self.ball["radius"] >= paddle["x"]
            and next_y + self.ball["radius"] >= paddle["y"]
            and next_y - self.ball["radius"] <= paddle["y"] + paddle["height"]
        ):
            relative_intersect_y = (
                self.ball["y"] - (paddle["y"] + paddle["height"] / 2)
            ) / (paddle["height"] / 2)
            bounce_angle = relative_intersect_y * (math.pi / 4)

            speed = math.sqrt(self.ball["speedX"] ** 2 + self.ball["speedY"] ** 2)
            direction = -1 if self.ball["x"] < self.WIDTH // 2 else 1

            self.ball["speedX"] = math.cos(bounce_angle) * direction * speed
            self.ball["speedY"] = math.sin(bounce_angle) * speed

            return True
        return False

    def get_state(self):
        """Return the current game state"""
        return {
            "left_paddle": self.left_paddle,
            "right_paddle": self.right_paddle,
            "ball": self.ball,
            "scores": self.scores,
            "countdown": max(0, self.countdown),
        }

    @database_sync_to_async
    def _send_score_update(self, is_player1):
        from apps.core.models import History

        try:
            matches = History.objects.filter(match_id=self.match_id)
            if not matches.exists():
                return

            match = matches.first()

            if is_player1:
                match.result_user += 1
            else:
                match.result_opponent += 1

            match.save()
        except Exception as e:
            print(f"Error updating score in database: {e}")
