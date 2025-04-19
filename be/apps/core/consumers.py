import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import GameState


class GameConsumer(AsyncWebsocketConsumer):
    games = {}  # Dictionary that will handle multiple games (key: match_id)

    async def connect(self):
        """Handle the connection of a new client"""
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.group_name = f"game_{self.match_id}"  # Each game has its own unique group
        self.user = self.scope["user"]  # Get the current user

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # If the game doesn't exist, create it
        if self.match_id not in self.__class__.games:
            self.__class__.games[self.match_id] = {
                "state": GameState(self.match_id),
                "players": set(),
                "loop_task": None,
                "left_player": None,
                "right_player": None,
            }
            self.__class__.games[self.match_id]["state"].start_game(self.match_id)

        game = self.__class__.games[self.match_id]

        # Assign position to the player if not assigned
        if game["left_player"] is None:
            game["left_player"] = self.user.id
            game["state"].set_left_player(self.user.id)
        elif game["right_player"] is None and game["left_player"] != self.user.id:
            game["right_player"] = self.user.id
            game["state"].set_right_player(self.user.id)

        game["players"].add(self)

        # Start loop if it's the first connection of the game
        if game["loop_task"] is None:
            await self.start_game_loop()

        # Send initial state to the client
        initial_state = game["state"].get_state()
        await self.send(json.dumps({"type": "init", **initial_state}))

    async def disconnect(self, _):
        """Handle the disconnection of a client"""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        if self.match_id in self.__class__.games:
            self.__class__.games[self.match_id]["players"].discard(self)

            # If there are no players in the game, delete it
            if not self.__class__.games[self.match_id]["players"]:
                game_state = self.__class__.games[self.match_id]["state"]

                # Stop the game if countdown is active or no players are connected
                if game_state.countdown is not None or not game_state.running:
                    game_state.running = False

                loop_task = self.__class__.games[self.match_id].get("loop_task")
                if loop_task:
                    loop_task.cancel()
                    try:
                        await loop_task
                    except asyncio.CancelledError:
                        pass

                del self.__class__.games[self.match_id]

    async def receive(self, text_data):
        """Handle the messages received from the clients"""
        data = json.loads(text_data)

        if data.get("type") == "key_event" and self.match_id in self.__class__.games:
            game = self.__class__.games[self.match_id]["state"]
            game.process_key_event(data["key"], data["is_pressed"])

            updated_state = game.get_state()
            await self.channel_layer.group_send(
                self.group_name, {"type": "game_update", "game_state": updated_state}
            )

    async def start_game_loop(self):
        """Start the game loop for the current game"""
        self.__class__.games[self.match_id]["state"].running = True
        self.__class__.games[self.match_id]["loop_task"] = asyncio.create_task(
            self._game_loop()
        )

    async def _game_loop(self):
        """Main game loop"""
        try:
            while (
                self.match_id in self.__class__.games
                and self.__class__.games[self.match_id]["state"].running
            ):
                game_state = self.__class__.games[self.match_id]["state"]

                # Stop the game loop if no players are connected
                if not self.__class__.games[self.match_id]["players"]:
                    game_state.running = False
                    break

                await game_state.update()
                state = game_state.get_state()
                await self.channel_layer.group_send(
                    self.group_name, {"type": "game_update", "game_state": state}
                )
                await asyncio.sleep(1 / 60)  # 60 FPS
        except asyncio.CancelledError:
            print(f"Game loop of {self.match_id} cancelled correctly")
        finally:
            if self.match_id in self.__class__.games:
                self.__class__.games[self.match_id]["loop_task"] = None
                self.__class__.games[self.match_id]["state"].running = False

    async def game_update(self, event):
        """Send game updates to the current game clients"""
        await self.send(text_data=json.dumps(event["game_state"]))
