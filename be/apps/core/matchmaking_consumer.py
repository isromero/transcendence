import json
import asyncio
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class MatchmakingConsumer(AsyncWebsocketConsumer):
    queue = []  # Cola de jugadores esperando partida

    async def connect(self):
        """ Maneja la conexión de un nuevo cliente """
        await self.accept()
        logger.info("Nuevo jugador buscando partida...")
        
        # Agregar jugador a la cola
        self.queue.append(self)
        await self.check_matchmaking()

    async def disconnect(self, close_code):
        """ Maneja la desconexión de un cliente """
        if self in self.queue:
            self.queue.remove(self)
        logger.info("Jugador desconectado del matchmaking.")

    async def check_matchmaking(self):
        """ Verifica si hay suficientes jugadores para iniciar una partida """
        while len(self.queue) >= 2:
            player1 = self.queue.pop(0)
            player2 = self.queue.pop(0)

            # 📌 Notificar a los jugadores que pueden crear una partida
            await player1.send(json.dumps({"type": "start_match"}))
            await player2.send(json.dumps({"type": "start_match"}))

            logger.info(f"🔗 Jugadores emparejados: {player1} y {player2} deben crear una partida.")
