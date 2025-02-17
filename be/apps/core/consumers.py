import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .game import GameState


class GameConsumer(AsyncWebsocketConsumer):
    game_state = GameState()  # Estado compartido del juego

    async def connect(self):
        # Unirse al grupo del juego
        await self.channel_layer.group_add("game_group", self.channel_name)
        await self.accept()
        # Enviar estado inicial
        await self.send(json.dumps(self.game_state.get_state()))

    async def disconnect(self, close_code):
        # Salir del grupo al desconectar
        await self.channel_layer.group_discard("game_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data["type"] == "key_event":
            self.game_state.process_key_event(data["key"], data["is_pressed"])
            # Actualizar todos los clientes
            await self.channel_layer.group_send(
                "game_group",
                {"type": "game_update", "game_state": self.game_state.get_state()},
            )

    async def game_update(self, event):
        # Enviar actualización a los clientes
        await self.send(text_data=json.dumps(event["game_state"]))
