import uuid
from fastapi import WebSocket, FastAPI, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
from dataclasses import dataclass

@dataclass
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        id = str(uuid.uuid4())
        self.active_connections[id] = websocket

        await self.send_message_to(websocket, json.dumps({"type": "connect", "id": id}))

    def disconnect(self, websocket: WebSocket):
        id = self.find_connection_id(websocket)
        del self.active_connections[id]
        return id

    def find_connection_id(self, websocket: WebSocket):
        val_list = list(self.active_connections.values())
        key_list = list(self.active_connections.keys())
        id = val_list.index(websocket)
        return key_list[id]

    async def send_message_to(self, ws: WebSocket, message: str):
        await ws.send_text(message)

    async def broadcast(self, message: str, sender: WebSocket):
        for connection in self.active_connections.values():
            if connection == sender:
                continue
            try:
                    await connection.send_text(message)
            except RuntimeError:
                    # Aquí podrías opcionalmente eliminar la conexión que falló
                    print(f"Error: la conexión {connection} está cerrada o ya completada.")



connection_manager = ConnectionManager()
app = FastAPI()

app.websocket("/messaging")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            # Recibe mensajes del cliente
            data = await websocket.receive_text()
            print("Received: ", data)
            # Envia el mensaje a todos los ws activos
            await connection_manager.broadcast(data, websocket)
    except WebSocketDisconnect:
        # Remueve la conexión de la lista ws
        id = connection_manager.disconnect(websocket)
        # Avisar al resto de clientes que un ws se desconectó
        await connection_manager.broadcast(json.dumps({
            "type": "disconnected", 
            "id": id
        }), websocket)

@app.get('/chat', response_class=HTMLResponse)
async def chat():
    path = Path("../routers/index.html")
    return path.read_text()


