from pydantic import BaseModel


# Модель токена данных
class TokenData(BaseModel):
    username: str | None = None


class AuthorizeRequest(BaseModel):
    username: str
    password: str
    client_id: str
    client_secret: str
    redirect_uri: str
    response_type: str
    scope: str


class AuthorizeResponse(BaseModel):
    code: str


class TokenRequest(BaseModel):
    username: str
    password: str
    grant_type: str
    scope: str
    client_id: str
    client_secret: str

    redirect_uri: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    scope: str
    client_id: str


class RegisterRequest(BaseModel):
    username: str
    password: str