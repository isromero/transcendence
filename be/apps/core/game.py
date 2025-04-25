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
        self.fps_cap = 60
        self.countdown = None  # Initially None until the game starts
        self.type_match = None
        self.current_user_id = None

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
        self.left_player_id = None
        self.right_player_id = None

    def start_game(self, match_id=None):
        """Init game with countdown"""
        if match_id:
            self.match_id = match_id
        self.countdown = 5.0  # Ensure it's a float
        self.running = True
        self.reset_ball()

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
        current_time = time.time()
        dt = min(current_time - self.last_update, 1 / 30)
        self.last_update = current_time

        if self.countdown is not None:
            self.countdown = max(0, self.countdown - dt)
            if self.countdown == 0:
                self.countdown = None

        # Stop the game if no players are connected
        if not self.running:
            return

        # Only allow paddle movement when the countdown is over
        if self.countdown is None:
            self._update_paddles(dt * self.fps_cap)

        if self.running and self.countdown is None and not self.game_over:
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

    async def _update_ball(self, dt):
        # Save the previous ball position
        prev_x = self.ball["x"]
        prev_y = self.ball["y"]

        # Calculate next position
        next_x = self.ball["x"] + self.ball["speedX"] * dt
        next_y = self.ball["y"] + self.ball["speedY"] * dt

        
        if next_x - self.ball["radius"] <= 0:
            self._last_scorer = "right"
            self.scores["right"] += 1
            if self.scores["right"] <= 5:
                await self._send_score_update(is_player1=False)
                if self.scores["right"] == 5:
                    self.running = False 
                    self.game_over = True
            self.reset_ball()
            return
        elif next_x + self.ball["radius"] >= self.WIDTH:
            
            self._last_scorer = "left"
            self.scores["left"] += 1
            if self.scores["left"] <= 5:
                await self._send_score_update(is_player1=True)
                if self.scores["left"] == 5:
                    self.running = False  
                    self.game_over = True
            self.reset_ball()
            return

        # Update position
        self.ball["x"] = next_x
        self.ball["y"] = next_y

        # Calculate the movement vector
        dx = self.ball["x"] - prev_x
        dy = self.ball["y"] - prev_y

        # Function to check paddle collision
        def check_paddle_collision(paddle):
            # Expand the collision area to include the complete ball movement
            expanded_paddle = {
                "x": paddle["x"] - self.ball["radius"],
                "y": paddle["y"] - self.ball["radius"],
                "width": paddle["width"] + self.ball["radius"] * 2,
                "height": paddle["height"] + self.ball["radius"] * 2,
            }

            # Check if the movement line intersects with the expanded paddle
            if (
                min(prev_x, self.ball["x"])
                <= expanded_paddle["x"] + expanded_paddle["width"]
                and max(prev_x, self.ball["x"]) >= expanded_paddle["x"]
                and min(prev_y, self.ball["y"])
                <= expanded_paddle["y"] + expanded_paddle["height"]
                and max(prev_y, self.ball["y"]) >= expanded_paddle["y"]
            ):

                # Calculate the exact collision point
                if dx != 0:  # Avoid division by zero
                    t = (
                        (expanded_paddle["x"] - prev_x) / dx
                        if self.ball["speedX"] > 0
                        else (expanded_paddle["x"] + expanded_paddle["width"] - prev_x)
                        / dx
                    )
                    t = max(0, min(1, t))
                    collision_y = prev_y + dy * t

                    if (
                        expanded_paddle["y"]
                        <= collision_y
                        <= expanded_paddle["y"] + expanded_paddle["height"]
                    ):
                        return True, collision_y
            return False, None

        # Check paddle collisions
        left_collision, left_y = check_paddle_collision(self.left_paddle)
        right_collision, right_y = check_paddle_collision(self.right_paddle)

        if left_collision and self.ball["speedX"] < 0:
            self._handle_paddle_collision(self.left_paddle, left_y, "left")
        elif right_collision and self.ball["speedX"] > 0:
            self._handle_paddle_collision(self.right_paddle, right_y, "right")

        # Collisions with top and bottom walls
        if (
            self.ball["y"] - self.ball["radius"] <= 0
            or self.ball["y"] + self.ball["radius"] >= self.HEIGHT
        ):
            self.ball["speedY"] = -self.ball["speedY"]
            self.ball["y"] = max(
                self.ball["radius"],
                min(self.HEIGHT - self.ball["radius"], self.ball["y"]),
            )

        # Check if there was a goal (after checking paddle collisions)
        if self.ball["x"] - self.ball["radius"] <= 0:
            # Ball crossed left boundary - Right player scores
            self._last_scorer = "right"
            self.scores["right"] += 1
            if self.scores["right"] <= 5:
                # Right player (player2) scored
                await self._send_score_update(
                    is_player1=False
                )  # The right player scored
            self.reset_ball()
            return  # Avoid updating position after resetting
        elif self.ball["x"] + self.ball["radius"] >= self.WIDTH:
            # Ball crossed right boundary - Left player scores
            self._last_scorer = "left"
            self.scores["left"] += 1
            if self.scores["left"] <= 5:
                # Left player (player1) scored
                await self._send_score_update(
                    is_player1=True
                )  # The left player scored
            self.reset_ball()
            return  # Avoid updating position after resetting

    def _handle_paddle_collision(self, paddle, collision_y, side):
        # Calculate the relative impact point on the paddle (-1 to 1)
        relative_intersect_y = (collision_y - (paddle["y"] + paddle["height"] / 2)) / (
            paddle["height"] / 2
        )

        # Calculate the bounce angle (limited by MIN_BOUNCE_ANGLE and MAX_BOUNCE_ANGLE)
        bounce_angle = relative_intersect_y * self.MAX_BOUNCE_ANGLE
        bounce_angle = max(
            -self.MAX_BOUNCE_ANGLE, min(self.MAX_BOUNCE_ANGLE, bounce_angle)
        )

        # Increase the speed
        speed = min(
            math.sqrt(self.ball["speedX"] ** 2 + self.ball["speedY"] ** 2)
            * self.BALL_ACCELERATION,
            self.MAX_BALL_SPEED,
        )

        # Update speeds - Corrected direction logic
        direction = 1 if side == "left" else -1
        self.ball["speedX"] = math.cos(bounce_angle) * direction * speed
        self.ball["speedY"] = math.sin(bounce_angle) * speed

        # Record last hit
        self.ball["last_hit"] = side

        # Record last hit
        self.ball["last_hit"] = side

    def process_key_event(self, key, is_pressed):
        """Handle keyboard events to move paddles"""
        # If it's a local match, allow all keys
        if self.type_match == "local":
            if key == "w" or key == "W":
                self.left_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
            elif key == "s" or key == "S":
                self.left_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0
            elif key == "ArrowUp":
                self.right_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
            elif key == "ArrowDown":
                self.right_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0

        # If it's a multiplayer match, only allow the keys for the current user
        elif self.type_match != "local":
            if (
                key == "w" or key == "W"
            ) and self.left_player_id == self.current_user_id:
                self.left_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
            elif (
                key == "s" or key == "S"
            ) and self.left_player_id == self.current_user_id:
                self.left_paddle["dy"] = self.PADDLE_SPEED if is_pressed else 0
            elif key == "ArrowUp" and self.right_player_id == self.current_user_id:
                self.right_paddle["dy"] = -self.PADDLE_SPEED if is_pressed else 0
            elif key == "ArrowDown" and self.right_player_id == self.current_user_id:
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
            "countdown": self.countdown,
        }

    def set_left_player(self, user_id):
        self.left_player_id = user_id

    def set_right_player(self, user_id):
        self.right_player_id = user_id

    @database_sync_to_async
    def _send_score_update(self, is_player1):
        from apps.core.models import History
        from django.db import transaction

        try:
            with transaction.atomic():
                matches = History.objects.filter(match_id=self.match_id)
                if not matches.exists():
                    print("No matches found for match_id:", self.match_id)
                    return

                for match in matches:
                    match_user_id = match.user_id.id
                    if match_user_id == self.left_player_id:
                        if is_player1:
                            match.result_user += 1
                        else:
                            match.result_opponent += 1
                    elif match_user_id == self.right_player_id:
                        if is_player1:
                            match.result_opponent += 1
                        else:
                            match.result_user += 1
                    else:
                        print(f"User ID {match_user_id} doesn't match either player!")
                    match.save()

        except Exception as e:
            print(f"Error updating scores in database: {e}")
