import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

import json
import asyncio
import uuid
from concurrent.futures import ThreadPoolExecutor
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import History, User


class MatchmakingConsumer(AsyncWebsocketConsumer):
    queue = []
    executor = ThreadPoolExecutor()

    async def connect(self):
        user_id = (
            self.scope["user"].id
            if self.scope.get("user") and self.scope["user"].is_authenticated
            else None
        )

        if not user_id:
            await self.close(code=4000)
            return

        await self.accept()

        user_in_queue = any(player[1] == user_id for player in self.queue)

        if not user_in_queue:
            self.queue.append((self, user_id))

        await self.check_matchmaking()

    async def disconnect(
        self, close_code
    ):  # don't delete close_code, it's required to not get an error
        """Handle client disconnection"""
        try:
            for i, player in enumerate(self.queue):
                if player[0] == self:
                    self.queue.pop(i)
                    break
        except Exception as e:
            print(f"Error during matchmaking disconnect: {e}")

    async def check_matchmaking(self):
        if len(self.queue) >= 2:
            # The first player in the queue is the left player
            player1_tuple = self.queue.pop(0)
            # The second player in the queue is the right player
            player2_tuple = self.queue.pop(0)

            player1_consumer, player1_id = player1_tuple
            player2_consumer, player2_id = player2_tuple

            match_id = await self.create_match(player1_id, player2_id)

            if not match_id:
                await player1_consumer.send(
                    json.dumps({"type": "error", "message": "Error creating match"})
                )
                await player2_consumer.send(
                    json.dumps({"type": "error", "message": "Error creating match"})
                )
                return

            await player1_consumer.send(
                json.dumps(
                    {"type": "start_match", "match_id": match_id, "position": "left"}
                )
            )
            await player2_consumer.send(
                json.dumps(
                    {"type": "start_match", "match_id": match_id, "position": "right"}
                )
            )

    async def create_match(self, player1_id, player2_id):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            self.executor, self.sync_create_match, player1_id, player2_id
        )

    def sync_create_match(self, player1_id, player2_id):
        try:
            match_id = str(uuid.uuid4())

            try:
                player1 = User.objects.get(id=player1_id)
                player2 = User.objects.get(id=player2_id)
            except User.DoesNotExist:
                return None

            History.objects.create(
                match_id=match_id,
                user_id=player1,
                opponent_id=player2,
                type_match="multiplayer",
                result_user=0,
                result_opponent=0,
            )

            History.objects.create(
                match_id=match_id,
                user_id=player2,
                opponent_id=player1,
                type_match="multiplayer",
                result_user=0,
                result_opponent=0,
            )

            return match_id
        except Exception as e:
            return None
