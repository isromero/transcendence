import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import GameState
import logging
import asyncio

logger = logging.getLogger(__name__)


class GameConsumer(AsyncWebsocketConsumer):
    game_state = GameState()
    _game_loop_task = None

    @classmethod
    async def start_game_loop(cls):
        """Inicia el game loop como método de clase"""
        if cls._game_loop_task is None:
            logger.info("Iniciando nuevo game loop")
            cls.game_state.running = True
            cls._game_loop_task = asyncio.create_task(cls._game_loop())

    @classmethod
    async def _game_loop(cls):
        """Game loop con mejor manejo de errores"""
        logger.info("Game loop iniciado")
        try:
            while cls.game_state.running:
                cls.game_state.update()
                state = cls.game_state.get_state()
                if hasattr(cls, "channel_layer"):
                    await cls.channel_layer.group_send(
                        "game_group", {"type": "game_update", "game_state": state}
                    )
                await asyncio.sleep(1 / 60)  # 60 FPS
        except asyncio.CancelledError:
            logger.info("Game loop cancelado correctamente")
        except Exception as e:
            logger.error(f"Error en game loop: {e}")
        finally:
            cls._game_loop_task = None
            cls.game_state.running = False


    async def connect(self):
        """Maneja la conexión de un nuevo cliente"""
        logger.info("Nuevo cliente conectando")
        await self.channel_layer.group_add("game_group", self.channel_name)
        await self.accept()

        self.__class__.channel_layer = self.channel_layer

        # Asegurar que el game loop solo se inicia si no está corriendo
        if not self._game_loop_task or self._game_loop_task.done():
            await self.start_game_loop()

        initial_state = self.game_state.get_state()
        logger.info(f"Estado inicial enviado: {initial_state}")
        await self.send(json.dumps(initial_state))


    async def disconnect(self, close_code):
        """Maneja la desconexión de un cliente"""
        logger.info(f"Cliente desconectado. Código: {close_code}")
        await self.channel_layer.group_discard("game_group", self.channel_name)

        # Esperar un poco para ver si aún hay clientes conectados
        await asyncio.sleep(0.1)

        group_size = len(self.channel_layer.groups.get("game_group", set()))

        if group_size == 0:
            logger.info("No quedan clientes conectados, deteniendo game loop")
            if self._game_loop_task:
                self._game_loop_task.cancel()
                try:
                    await self._game_loop_task
                except asyncio.CancelledError:
                    logger.info("Game loop detenido correctamente")
                self._game_loop_task = None
                self.game_state.running = False


    async def receive(self, text_data):
        """Maneja los mensajes recibidos de los clientes"""
        data = json.loads(text_data)
        logger.info(f"Mensaje recibido: {data}")

        if data["type"] == "key_event":
            self.game_state.process_key_event(data["key"], data["is_pressed"])

    async def game_update(self, event):
        """Envía actualizaciones del juego a los clientes"""
        await self.send(text_data=json.dumps(event["game_state"]))
