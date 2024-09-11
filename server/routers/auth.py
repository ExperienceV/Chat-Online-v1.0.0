from fastapi import APIRouter, status, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
from models import register_model, login_model
from database.auth_queries import user_create, user_login
from JWT.functions_jwt import *

auth_rt = APIRouter()


@auth_rt.get("/chat", response_class=HTMLResponse)
async def register_client():
    path = Path("../client/static/html/chat.html")
    return path.read_text()

@auth_rt.get("/login", response_class=HTMLResponse)
async def login_client():
    path = Path("../client/static/html/login.html")
    return path.read_text()

@auth_rt.post("/login_request")
async def login_server(login: login_model):
    response: dict | bool = await user_login(
        user_name=login.user_name,
        user_password=login.user_password
    )

    print(login.user_name)

    if not response:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Oooops, parece que hubo un problema."
        )

    token_create: str = write_token(response)
    raise HTTPException(status_code=200, detail=token_create)

@auth_rt.get("/register", response_class=HTMLResponse)
async def register_client():
    path = Path("../client/static/html/register.html")
    return path.read_text()

@auth_rt.post("/register_request")
async def register_server(register: register_model):
    
    if not register.user_password == register.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Las contraseñas no coinciden."
        )
    
    response: dict | bool = await user_create(
        user_name= register.user_name,
        user_password= register.user_password
    )


    if not response:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Oooops, parece que hubo un problema."
        )

    token_create: str = write_token(response)
    
    raise HTTPException(status_code=200, detail=token_create)
