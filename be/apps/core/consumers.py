import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
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

        from apps.core.models import History

        @database_sync_to_async
        def get_match_data():
            matches = list(
                History.objects.filter(match_id=self.match_id)
                .order_by("id")
                .select_related("user_id")
            )
            if not matches:
                return None, None, None

            match = matches[0]

            if match.type_match.startswith("tournament"):
                player1 = matches[0].user_id
                player2 = matches[1].user_id if len(matches) > 1 else None
            else:
                player1 = matches[0].user_id
                player2 = matches[1].user_id if len(matches) > 1 else None

            return match, player1, player2

        match_data = await get_match_data()
        if not match_data or not match_data[0]:
            await self.close()
            return

        match, player1, player2 = match_data

        # If the game doesn't exist, create it
        if self.match_id not in self.__class__.games:
            self.__class__.games[self.match_id] = {
                "state": GameState(self.match_id),
                "players": set(),
                "loop_task": None,
                "left_player": None,
                "right_player": None,
            }
            game_state = self.__class__.games[self.match_id]["state"]
            game_state.type_match = match.type_match
            game_state.start_game(self.match_id)

        game = self.__class__.games[self.match_id]

        # For tournaments and multiplayer, assign positions based on order
        if match.type_match in [
            "multiplayer",
            "tournament_quarter",
            "tournament_semi",
            "tournament_final",
        ]:
            if player1 and player2:
                first_player_id = player1.id
                second_player_id = player2.id

                # Assign positions consistently
                game["left_player"] = first_player_id
                game["right_player"] = second_player_id
                game["state"].set_left_player(first_player_id)
                game["state"].set_right_player(second_player_id)

        # Assign position to the player if not assigned (for non-multiplayer games)
        elif game["left_player"] is None:
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
            game.current_user_id = self.user.id
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

                
                if not self.__class__.games[self.match_id]["players"] or game_state.game_over:
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
