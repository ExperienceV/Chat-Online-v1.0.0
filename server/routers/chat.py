import json
from fastapi import APIRouter, HTTPException, status, Header, Depends, WebSocket, WebSocketDisconnect
from JWT.functions_jwt import validate_token
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from typing import List
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database.messages_queries import  save_message, whole_messages

chat_rts = APIRouter()
security = HTTPBearer()

from dotenv import load_dotenv

@chat_rts.get("/chat", response_class=HTMLResponse)
async def chat():
    path = Path("../client/static/html/auth.html")
    return path.read_text()

@chat_rts.get("/chat_request")
async def chat_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token: str = credentials.credentials
    response: dict | JSONResponse = validate_token(token=token)

    if isinstance(response, JSONResponse):
        json_data = json.loads(response.body.decode('UTF-8'))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=json_data['message']
        )
    
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail="No problem!"
    )

@chat_rts.get("/verify/token")
async def token_verify(Authorization: str = Header(None)) -> str:
    token: str = Authorization.split(" ")[1]
    return validate_token(token=token, output=True)




class ConnectionManager:
    """
    Clase para gestionar las conexiones WebSocket activas y manejar la 
    difusión de mensajes a todos los clientes conectados.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """
        Acepta una nueva conexión WebSocket y la añade a la lista de 
        conexiones activas.

        Args:
            websocket (WebSocket): El WebSocket que se está conectando.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """
        Elimina una conexión WebSocket de la lista de conexiones activas.

        Args:
            websocket (WebSocket): El WebSocket que se está desconectando.
        """
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        """
        Envía un mensaje a un cliente específico a través de su conexión 
        WebSocket.

        Args:
            message (str): El mensaje a enviar.
            websocket (WebSocket): El WebSocket destinatario del mensaje.
        """
        await websocket.send_text(message)

    async def broadcast(self, message: str, sender: WebSocket):
        """
        Envía un mensaje a todos los clientes conectados a través de sus 
        conexiones WebSocket.

        Args:
            message (str): El mensaje a enviar a todos los clientes.
        """
        for connection in self.active_connections:
                if connection != sender:
                    try:
                        await connection.send_text(message)
                    except RuntimeError:
                        # Aquí podrías opcionalmente eliminar la conexión que falló
                        print(f"Error: la conexión {connection} está cerrada o ya completada.")
                
connection_manager = ConnectionManager()

@chat_rts.websocket("/ws_chat")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    
    try:
        while True:
            data_fetch: str = await websocket.receive_text()
            data_dict: dict = json.loads(data_fetch)
            message: str = data_dict["message"]
            token: str = data_dict["token"]
            
            token_decode: bool | JSONResponse = await json_data(token=token)
            user: str = token_decode["user_name"]
            
            # Guardado de mensajes con identificador.
            user_id: int = token_decode["id"]
            await save_message(user_id, message)

            # Envio de mensaje a todas las conexiones activas.
            send_message = f"{user}: {message}"
            await connection_manager.broadcast(send_message, websocket)

    except WebSocketDisconnect as e:
        print(e)


@chat_rts.get("/load_messages")
async def load_messages(Authorization: str = Header(None)) -> dict:
    token: str = Authorization.split(" ")[1]
    user: dict = await json_data(token)
    messages: list = await whole_messages()
  
    "Relacionar ID de mensaje con ID de usuario"

    msg_dict: dict = {}

    for message in messages:
        if message[1] == user['id']:
            msg_dict[message[0]] = {
                'type' : 'emisor',
                'message' : message[2],
                'timestamp' : message[3]
            }
        else:
            msg_dict[message[0]] = {
                'type' : 'receiver',
                'message' : message[2],
                'timestamp' : message[3]
            }
            
    return msg_dict



async def json_data(token) -> bool | JSONResponse:
    verify_token_response = validate_token(token=token)
    
    if isinstance(verify_token_response, JSONResponse):
        return False
    
    return verify_token_response



