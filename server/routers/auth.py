from fastapi import APIRouter, status, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
from models import auth_model
from database.auth_queries import user_create
from database.data_queries import user_data
from JWT.functions_jwt import *

auth_rt = APIRouter()

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from pathlib import Path

auth_rt = APIRouter()

@auth_rt.get('/join', response_class=HTMLResponse)
async def auth():
    path = Path("../client/static/html/join.html")
    return path.read_text(encoding="utf-8")

@auth_rt.post('/authenticate_process')
async def auth_process(form: auth_model):
    """
    Procesa la autenticación del usuario.

    Esta función recibe las credenciales del usuario y verifica su cuenta.
    Si el usuario no existe, se crea uno nuevo. Si la autenticación es exitosa,
    se devuelve un mensaje correspondiente.

    Args:
        form (auth_model): Modelo que contiene el nombre de usuario y la contraseña.

    Raises:
        HTTPException: Si hay un problema con la autenticación o la creación de la cuenta.
    """
    name, password = form.user_name, form.user_password
    response = await verify_account(form.user_name, form.user_password)

    if not response:
        raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='Contraseña incorrecta'
            )

    raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=response
        )
    
async def verify_account(username, password):
    """
    Verifica la cuenta del usuario.

    Esta función comprueba si el usuario existe y si la contraseña es correcta.
    Si el usuario no existe, se crea uno nuevo. Si la contraseña es incorrecta,
    se lanza una excepción.

    Args:
        username (str): El nombre de usuario a verificar.
        password (str): La contraseña del usuario.

    Raises:
        HTTPException: Si el usuario no existe y no se puede crear, si la contraseña
                       es incorrecta o si la autenticación es exitosa.
    """
    try:
        response = await user_data(username)
        #print(response)

        if not response:
            response_create = await user_create(username, password)
            token_create: str = write_token(response_create)

            if isinstance(response_create, dict):
                return token_create
        
        if response['user_password'] != password:
            return False


        token_create: str = write_token(response)
        return token_create
    except Exception as e:
        print(e)
        