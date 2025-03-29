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
from .models import History, User


logger = logging.getLogger(__name__)

class MatchmakingConsumer(AsyncWebsocketConsumer):
    queue = []  # Cambiado a lista para almacenar tuplas (consumer, user_id)
    executor = ThreadPoolExecutor()

    async def connect(self):
        # Obtener el usuario del scope
        user_id = self.scope["user"].id if self.scope.get("user") and self.scope["user"].is_authenticated else None
        
        if not user_id:
            await self.close(code=4000)
            return
        
        await self.accept()
        
        # Verificar si el usuario ya está en cola
        user_in_queue = any(player[1] == user_id for player in self.queue)
        
        if not user_in_queue:
            self.queue.append((self, user_id))
            logger.info(f"✅ Jugador con ID {user_id} añadido al matchmaking.")
        else:
            logger.warning(f"⚠️ Jugador con ID {user_id} ya está en la cola.")
        
        await self.check_matchmaking()

    async def disconnect(self, close_code):
        # Buscar y eliminar el jugador de la cola
        for i, player in enumerate(self.queue):
            if player[0] == self:
                user_id = player[1]
                self.queue.pop(i)
                logger.info(f"Jugador con ID {user_id} desconectado del matchmaking.")
                break
        
    async def check_matchmaking(self):
        if len(self.queue) >= 2:
            player1_tuple = self.queue.pop(0)  # Obtenemos la tupla (consumer, user_id)
            player2_tuple = self.queue.pop(0)
            
            player1_consumer, player1_id = player1_tuple
            player2_consumer, player2_id = player2_tuple

            match_id = await self.create_match(player1_id, player2_id)

            if not match_id:
                logger.error("❌ Error al crear la partida.")
                await player1_consumer.send(json.dumps({"type": "error", "message": "Error al crear la partida"}))
                await player2_consumer.send(json.dumps({"type": "error", "message": "Error al crear la partida"}))
                return

            logger.info(f"🎮 Match ID generado: {match_id}")

            await player1_consumer.send(json.dumps({"type": "start_match", "match_id": match_id, "player": "left"}))
            await player2_consumer.send(json.dumps({"type": "start_match", "match_id": match_id, "player": "right"}))

    async def create_match(self, player1_id, player2_id):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.sync_create_match, player1_id, player2_id)

    def sync_create_match(self, player1_id, player2_id):
        try:
            match_id = str(uuid.uuid4())
            
            try:
                player1 = User.objects.get(id=player1_id)
                player2 = User.objects.get(id=player2_id)
            except User.DoesNotExist:
                logger.error(f"❌ No se encontraron los usuarios con IDs: {player1_id}, {player2_id}")
                return None

            # Crear dos registros, uno desde la perspectiva de cada jugador
            # Registro para player1
            History.objects.create(
                match_id=match_id,
                user_id=player1,
                opponent_id=player2,
                type_match="match",
                local_match=True,  # Mantenido en True como solicitaste
                result_user=0,
                result_opponent=0,
            )
            
            # Registro para player2
            History.objects.create(
                match_id=match_id,
                user_id=player2,
                opponent_id=player1,
                type_match="match",
                local_match=True,  # Mantenido en True como solicitaste
                result_user=0,
                result_opponent=0,
            )

            logger.info(f"✅ Partida creada con ID: {match_id} entre jugadores {player1_id} y {player2_id}")
            return match_id
        except Exception as e:
            logger.error(f"❌ Error creando la partida: {e}")
            return None