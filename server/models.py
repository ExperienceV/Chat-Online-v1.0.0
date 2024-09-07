from pydantic import BaseModel


class register_model(BaseModel):
    user_name: str
    user_password: str
    confirm_password: str

class login_model(BaseModel):
    user_name: str
    user_password: str

class token_model(BaseModel):
    token: str
