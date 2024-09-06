from fastapi.responses import JSONResponse
from jwt import encode, decode
from jwt import exceptions
from datetime import datetime, timedelta
from os import getenv

def expire_date(days: int) -> int:
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date


def write_token(data: dict) -> str:
    secret_key = getenv("SECRET")
    
    if not isinstance(secret_key, str) or not secret_key:
        raise ValueError("La clave secreta debe ser una cadena no vacía.")
    
    if not isinstance(data, dict):
        raise ValueError("Los datos deben ser un diccionario.")
    
    try:
        token = encode(payload={**data, "exp": expire_date(2)}, key=secret_key, algorithm="HS256")
        print(token)
    except Exception as e:
        raise RuntimeError("Error al generar el token: " + str(e))
    
    return token


def validate_token(token: str, output: bool = False) -> JSONResponse:
    secret_key = getenv("SECRET")
    
    if not secret_key:
        return JSONResponse(content={"message": "Secret key is not set"}, status_code=500)

    try:
        decoded_token = decode(token, key=secret_key, algorithms=["HS256"])
        
        if output:
            print(decoded_token)
        
        return decoded_token 

    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": 'Token Expired'}, status_code=401)
    except exceptions.DecodeError:
        return JSONResponse(content={"message": 'Invalid Token'}, status_code=401)
    

