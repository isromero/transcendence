import json
import asyncio
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import GameState

logger = logging.getLogger(__name__)


class GameConsumer(AsyncWebsocketConsumer):
    games = {}  # Diccionario que manejará múltiples partidas (clave: match_id)
    
    async def connect(self):
        """Maneja la conexión de un nuevo cliente"""
        self.match_id = self.scope["url_route"]["kwargs"]["match_id"]
        self.group_name = f"game_{self.match_id}"  # Cada partida tiene su grupo único

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        logger.info(f"Cliente conectado a la partida {self.match_id}")

        # Si la partida no existe, la creamos
        if self.match_id not in self.__class__.games:
            self.__class__.games[self.match_id] = {
                "state": GameState(self.match_id),
                "players": set(),
                "loop_task": None,
            }

        # Añadir jugador a la partida
        self.__class__.games[self.match_id]["players"].add(self)

        # Iniciar loop si es la primera conexión de la partida
        if self.__class__.games[self.match_id]["loop_task"] is None:
            await self.start_game_loop()

        # Enviar estado inicial al cliente
        initial_state = self.__class__.games[self.match_id]["state"].get_state()
        await self.send(json.dumps({"type": "init", "state": initial_state}))

    async def disconnect(self, close_code):
        """Maneja la desconexión de un cliente"""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        logger.info(f"Cliente desconectado de la partida {self.match_id}")

        # Eliminar jugador de la partida
        if self.match_id in self.__class__.games:
            self.__class__.games[self.match_id]["players"].discard(self)

            # Si no hay jugadores en la partida, la eliminamos
            if not self.__class__.games[self.match_id]["players"]:
                logger.info(f"No quedan jugadores en la partida {self.match_id}, deteniendo el juego...")
                if self.__class__.games[self.match_id]["loop_task"]:
                    self.__class__.games[self.match_id]["loop_task"].cancel()
                    try:
                        await self.__class__.games[self.match_id]["loop_task"]
                    except asyncio.CancelledError:
                        logger.info(f"Game loop de {self.match_id} detenido correctamente")

                del self.__class__.games[self.match_id]  # Eliminar la partida

    async def receive(self, text_data):
        """Maneja los mensajes recibidos de los clientes"""
        data = json.loads(text_data)

        if data.get("type") == "key_event" and self.match_id in self.__class__.games:
            game = self.__class__.games[self.match_id]["state"]
            game.process_key_event(data["key"], data["is_pressed"])

            # ✅ Enviar estado actualizado tras cada evento de teclado
            updated_state = game.get_state()
            await self.channel_layer.group_send(self.group_name, {
                "type": "game_update",
                "game_state": updated_state
            })


    async def start_game_loop(self):
        """Inicia el loop de juego para la partida actual"""
        self.__class__.games[self.match_id]["state"].running = True
        self.__class__.games[self.match_id]["loop_task"] = asyncio.create_task(self._game_loop())

    async def _game_loop(self):
        """Loop principal del juego"""
        try:
            while self.match_id in self.__class__.games and self.__class__.games[self.match_id]["state"].running:
                self.__class__.games[self.match_id]["state"].update()
                state = self.__class__.games[self.match_id]["state"].get_state()
                await self.channel_layer.group_send(self.group_name, {"type": "game_update", "game_state": state})
                await asyncio.sleep(1 / 60)  # 60 FPS
        except asyncio.CancelledError:
            logger.info(f"Game loop de {self.match_id} cancelado correctamente")
        finally:
            if self.match_id in self.__class__.games:
                self.__class__.games[self.match_id]["loop_task"] = None
                self.__class__.games[self.match_id]["state"].running = False

    async def game_update(self, event):
        """Envía actualizaciones del juego a los clientes de la partida actual"""
        await self.send(text_data=json.dumps(event["game_state"]))
