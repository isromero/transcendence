import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PongConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Jugador conectado.")

    async def disconnect(self, close_code):
        print("Jugador desconectado.")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Datos recibidos:", data)

        # Enviar actualización a los clientes
        await self.send(text_data=json.dumps({
            "message": "Actualización de juego",
            "data": data
        }))
