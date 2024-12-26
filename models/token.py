from pydantic import BaseModel


# Модель токена
class Token(BaseModel):
    access_token: str
    token_type: str
    scope: str
    client_id: str


# Модель токена данных
class TokenData(BaseModel):
    username: str | None = None

class Authorize(BaseModel):
    username: str
    password: str
    client_id: str
    client_secret: str
    redirect_uri: str
    response_type: str
    scope: str