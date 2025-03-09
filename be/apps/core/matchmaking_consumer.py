import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

import json
import asyncio
import logging
import uuid
from concurrent.futures import ThreadPoolExecutor
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import History, User  # Ajusta el import según tu estructura


logger = logging.getLogger(__name__)

class MatchmakingConsumer(AsyncWebsocketConsumer):
    queue = set()
    executor = ThreadPoolExecutor()

    async def connect(self):
        await self.accept()
        if self not in self.queue:
            self.queue.add(self)
            logger.info("✅ Nuevo jugador añadido al matchmaking.")
        else:
            logger.warning("⚠️ Este jugador ya está en la cola.")
        await self.check_matchmaking()

    async def disconnect(self, close_code):
        if self in self.queue:
            self.queue.remove(self)
        logger.info("Jugador desconectado del matchmaking.")

    async def check_matchmaking(self):
        if len(self.queue) >= 2:
            player1 = self.queue.pop()
            player2 = self.queue.pop()

            match_id = await self.create_match()

            if not match_id:
                logger.error("❌ Error al crear la partida.")
                await player1.send(json.dumps({"type": "error", "message": "Error al crear la partida"}))
                await player2.send(json.dumps({"type": "error", "message": "Error al crear la partida"}))
                return

            logger.info(f"🎮 Match ID generado: {match_id}")

            await player1.send(json.dumps({"type": "start_match", "match_id": match_id, "player": "left"}))
            await player2.send(json.dumps({"type": "start_match", "match_id": match_id, "player": "right"}))

    async def create_match(self):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.sync_create_match)

    def sync_create_match(self):
        try:
            match_id = str(uuid.uuid4())
            user = User.objects.first()  # Ajusta según cómo obtienes los jugadores

            if not user:
                logger.error("❌ No se encontró un usuario válido.")
                return None

            History.objects.create(
                match_id=match_id,
                user_id=user,
                opponent_id=user,
                type_match="match",
                local_match=True,
                result_user=0,
                result_opponent=0,
            )

            logger.info(f"✅ Partida creada con ID: {match_id}")
            return match_id
        except Exception as e:
            logger.error(f"❌ Error creando la partida: {e}")
            return None