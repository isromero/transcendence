import json
import asyncio
import logging
import uuid
import requests  # Usamos requests en lugar de aiohttp
from concurrent.futures import ThreadPoolExecutor
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class MatchmakingConsumer(AsyncWebsocketConsumer):
    queue = set()
    executor = ThreadPoolExecutor()  # Para ejecutar requests en un hilo separado

    async def connect(self):
        """ Maneja la conexión de un nuevo cliente """
        await self.accept()

        if self not in self.queue:
            self.queue.add(self)
            logger.info("✅ Nuevo jugador añadido al matchmaking.")
        else:
            logger.warning("⚠️ Este jugador ya está en la cola.")

        await self.check_matchmaking()

    async def disconnect(self, close_code):
        """ Maneja la desconexión de un cliente """
        if self in self.queue:
            self.queue.remove(self)
        logger.info("Jugador desconectado del matchmaking.")

    async def check_matchmaking(self):
        """ Verifica si hay suficientes jugadores para iniciar una partida """
        if len(self.queue) >= 2:
            player1 = self.queue.pop()
            player2 = self.queue.pop()

            # ✅ Crear la partida en el backend usando requests (en un hilo separado)
            match_id = await self.create_match()

            if not match_id:
                logger.error("❌ Error al crear la partida en el backend.")
                await player1.send(json.dumps({"type": "error", "message": "Error al crear la partida"}))
                await player2.send(json.dumps({"type": "error", "message": "Error al crear la partida"}))
                return

            logger.info(f"🎮 Match ID generado desde el backend: {match_id}")

            # ✅ Enviar el mismo match_id a ambos jugadores
            await player1.send(json.dumps({"type": "start_match", "match_id": match_id}))
            await player2.send(json.dumps({"type": "start_match", "match_id": match_id}))

    async def create_match(self):
        """ Llama al backend para crear la partida usando requests en un hilo separado """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, self.sync_create_match)

    def sync_create_match(self):
        """ Método síncrono para hacer la solicitud al backend con requests """
        url = "http://localhost:8000/api/history"
        payload = {"local_match": True}  # ✅ Ahora es un diccionario válido
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response_data = response.json()

            if response.status_code == 201:
                return response_data["data"]["match_id"]
            else:
                logger.error(f"❌ Error en la API: {response_data}")
                return None
        except Exception as e:
            logger.error(f"❌ Error en la solicitud al backend: {e}")
            return None
