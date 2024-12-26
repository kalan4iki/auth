from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pony.orm import db_session

from db import Client, User, initialize_db, pwd_context
from depends import get_current_user
from models.token import Token, Authorize
from settings import setting
from utils import get_url
from utils.keys import check_keys_file_exists, get_key
from utils.token import create_access_token

# Приложение
app = FastAPI()


# Функции инициализации
check_keys_file_exists()
initialize_db()


# Эндпоинт для регистрации пользователя
@app.post("/register")
async def register(username: str, password: str):
    with db_session:
        user = User.get(username=username)
        if user:
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed_password = pwd_context.hash(password)
        User(username=username, hashed_password=hashed_password)
    return {"message": "User created successfully"}


# Эндпоинт для авторизации
@app.post("/user/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with db_session:
        user = User.get(username=form_data.username)
        if not user:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )
        if not user.verify_password(form_data.password):
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )
        access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
    return {"access_token": access_token, "token_type": "bearer"}


# Эндпоинт для информации о пользователе
@app.get("/user/userinfo", response_model=dict)
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}


# Эндпоинт для конфигурации OpenID Connect
@app.get("/.well-known/openid-configuration")
async def openid_configuration():
    base_url = get_url()
    return {
        "issuer": base_url,
        "authorization_endpoint": base_url + "/user/authorize",
        "token_endpoint": base_url + "/user/token",
        "userinfo_endpoint": base_url + "/user/userinfo",
        "jwks_uri": base_url + "/.well-known/jwks.json",
    }


# Эндпоинт для набора открытых ключей
@app.get("/.well-known/jwks.json")
async def jwks():
    public_key = get_key('public', False)
    return {
        "keys": [
            {
                "kty": "RSA",
                "n": public_key.public_numbers().n.to_bytes(256, byteorder="big").hex(),
                "e": public_key.public_numbers().e.to_bytes(3, byteorder="big").hex(),
                "kid": "general",
            }
        ]
    }


# Эндпоинт для авторизации клиента
@app.post("/user/authorize")
async def authorize(data: Authorize):
    with db_session:
        client: Client = Client.get(client_id=data.client_id)
        if not client:
            raise HTTPException(status_code=401, detail="Invalid client ID")
        if client.client_secret != data.client_secret:
            raise HTTPException(status_code=401, detail="Invalid client secret")
        # if client.redirect_uri != data.redirect_uri:
        #     raise HTTPException(status_code=401, detail="Invalid redirect URI")
        
    return {"code": "authorization_code"}


# Эндпоинт для токена доступа
@app.post("/user/token")
async def token(code: str, grant_type: str, redirect_uri: str, client_id: str, client_secret: str):
    with db_session:
        client = Client.get(client_id=client_id)
        if not client:
            raise HTTPException(status_code=401, detail="Invalid client")
        if client.client_secret != client_secret:
            raise HTTPException(status_code=401, detail="Invalid client secret")
        # TODO: Добавить проверку адреса перехода
        # TODO: Добавить проверку срока действия кода
        # TODO: Добавить проверку пользовательского имени и пароля
        # TODO: Добавить проверку существования пользователя
        # TODO: Добавить проверку подлинности кода
        # TODO: Добавить выдачу токена доступа
        # TODO: Добавить выдачу информации о пользователе
        # TODO: Добавить выдачу информации о клиенте
        # TODO: Добавить выдачу информации о сроке действия токена
        # TODO: Добавить выдачу информации о местоположении клиента
        # TODO: Добавить выдачу информации о соответствии требованиям OAuth 2.0

    return {
        "access_token": "access_token",
        "token_type": "bearer",
        "scope": client.scope,
        "client_id": client_id,
    }
