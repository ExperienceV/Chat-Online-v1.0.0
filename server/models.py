from pydantic import BaseModel


class token_model(BaseModel):
    token: str

class auth_model(BaseModel):
    user_name: str
    user_password: str
