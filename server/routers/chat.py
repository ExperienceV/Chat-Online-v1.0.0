from database.data_queries import user_data
import json
from fastapi import APIRouter, HTTPException, status, Header, Depends, WebSocket, WebSocketDisconnect
from JWT.functions_jwt import validate_token
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from database.messages_queries import  save_message, whole_messages

chat_rts = APIRouter()
security = HTTPBearer()

from dotenv import load_dotenv

@chat_rts.get("/chat", response_class=HTMLResponse)
async def chat():
    path = Path("../client/static/html/chat.html")
    return path.read_text()

@chat_rts.get("/chat_request")
async def chat_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    response = validate_token(token=token)

    if isinstance(response, JSONResponse):
        json_data = json.loads(response.body.decode('UTF-8'))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=json_data['message']
        )
    
    return HTTPException(
        status_code=status.HTTP_200_OK,
        detail="No problem!"
    )

@chat_rts.get("/verify/token")
async def token_verify(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
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
    
    cons = connection_manager.active_connections
    print(cons)

    try:
        #await websocket.accept()

        while True:
            data_fetch = await websocket.receive_text()
            data_dict = json.loads(data_fetch)
            message = data_dict["message"]
            token = data_dict["token"]
            
            token_decode = await json_data(token=token)
            user = token_decode["user_name"]
            
            # Guardado de mensajes con identificador.
            user_id = token_decode["id"]
            await save_message(user_id, message)

            send_message = f"{user}: {message}"
            #await websocket.send_text(f"{user}: {data_message}")
            await connection_manager.broadcast(send_message, websocket)
    except WebSocketDisconnect as e:
        print(e)


@chat_rts.get("/load_messages")
async def load_messages(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]

    if token == 'null':
        print('No estás autenticado correctamente')
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    user = await json_data(token)
    messages = await whole_messages()

    "Relacionar ID de mensaje con ID de usuario"

    msg_list = []

    for message in messages:
        if message[1] == user['id']:
            msg_list.append(f"true {message[2]}")
        else:
            msg_list.append(f"false {user['user_name']}: {message[2]}")

    return msg_list

async def json_data(token):
    verify_token_response = validate_token(token=token, output=False)
    
    if isinstance(verify_token_response, JSONResponse):
        return False
    
    return verify_token_response