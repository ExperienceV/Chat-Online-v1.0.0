from database.data_queries import user_data
import json
from fastapi import APIRouter, HTTPException, status, Header, Depends, WebSocket, WebSocketDisconnect
from JWT.functions_jwt import validate_token
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from database.messages_queries import save_message, whole_messages

chat_rts = APIRouter()
security = HTTPBearer()

@chat_rts.get("/chat", response_class=HTMLResponse)
async def chat():
    """
    Renderiza la página de chat.

    Esta función lee el archivo HTML de la página de chat
    y lo devuelve como respuesta.

    Returns:
        str: Contenido del archivo HTML de la página de chat.
    """
    path = Path("../client/static/html/chat.html")
    return path.read_text()

@chat_rts.get("/chat_request")
async def chat_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifica las credenciales del cliente para acceder al chat.

    Esta función valida el token proporcionado en las credenciales
    y devuelve un estado según la validez del token.

    Args:
        credentials (HTTPAuthorizationCredentials): Credenciales de autorización
                                                    que contienen el token.

    Raises:
        HTTPException: Si el token es inválido, se lanza una excepción
                       con un código de estado 401.

    Returns:
        HTTPException: Si el token es válido, se lanza una excepción
                       con un código de estado 200.
    """
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
    """
    Maneja la conexión WebSocket para el chat.

    Esta función establece una conexión WebSocket, recibe mensajes
    del cliente y los difunde a todos los demás clientes conectados.

    Args:
        websocket (WebSocket): La conexión WebSocket del cliente.
    """
    await connection_manager.connect(websocket)
    try:
        while True:
            # Esperar a recibir un mensaje del websocket
            data_fetch = await websocket.receive_text()
            data_dict = json.loads(data_fetch)
            # Extraer el mensaje y el token del diccionario
            message = data_dict.get("message")
            token = data_dict.get("token")
            # Decodificar el token para obtener información del usuario
            token_decode = await json_data(token=token)
            user_name = token_decode.get("user_name")
            user_id = token_decode.get("id")
            # Guardar el mensaje con el identificador del usuario
            await save_message(user_id, message)
            # Formatear el mensaje para enviar
            formatted_message = f"{user_name}: {message}"
            # Broadcast del mensaje a todas las conexiones activas
            await connection_manager.broadcast(formatted_message, websocket)
    except WebSocketDisconnect as e:
        print(f"WebSocket desconectado: {e}")

@chat_rts.get("/load_messages")
async def load_messages(Authorization: str = Header(None)):
    """
    Carga los mensajes para el usuario autenticado.

    Esta función verifica el token de autorización y carga los mensajes
    asociados al usuario.

    Args:
        Authorization (str): Token de autorización del usuario.

    Raises:
        HTTPException: Si el token es inválido o el usuario no está autenticado.

    Returns:
        List[str]: Lista de mensajes cargados para el usuario.
    """
    token = Authorization.split(" ")[1]
    if token == 'null':
        print('No estás autenticado correctamente')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    user = await json_data(token)
    messages = await whole_messages()
    
    # Relacionar ID de mensaje con ID de usuario
    msg_list = []
    for message in messages:
        if message[1] == user['id']:
            msg_list.append(f"true {message[2]}")
        else:
            msg_list.append(f"false {user['user_name']}: {message[2]}")
    
    return msg_list

async def json_data(token):
    """
    Verifica y decodifica el token JWT.

    Esta función valida el token y devuelve los datos del usuario
    si el token es válido.

    Args:
        token (str): El token JWT a verificar.

    Returns:
        dict | bool: Datos del usuario si el token es válido, False en caso contrario.
    """
    verify_token_response = validate_token(token=token, output=False)
    if isinstance(verify_token_response, JSONResponse):
        return False
    return verify_token_response