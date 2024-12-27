from datetime import timedelta

from fastapi import Depends
from fastapi.routing import APIRouter
from pony.orm import db_session

from depends import get_current_user
from models import ErrorMessage
from models.token import TokenRequest, TokenResponse
from settings import setting
from utils import clients, token, users

user_router = APIRouter(prefix="/user", tags=['user'])


# Эндпоинт для авторизации
@user_router.post(
    "/token",
    response_model=TokenResponse,
    responses={401: {"model": ErrorMessage}},
)
async def login_for_access_token(data: TokenRequest = Depends()):
    with db_session:
        # Блок проверки клиента
        client = clients.get_client(
            client_id=data.client_id,
            redirect_uri=data.redirect_uri,
            client_secret=data.client_secret,
            secret_check=True,
        )

        # Блок проверки пользователя
        user = users.get_user(username=data.username, password=data.password)

        # Блок генерации токена
        access_token_expires = timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = token.create_access_token(
            client=client,
            user=user,
            data={"sub": user.username},
            expires_delta=access_token_expires,
        )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "scope": data.scope,
        "client_id": data.client_id,
    }


# Эндпоинт для информации о пользователе
@user_router.get("/userinfo", response_model=dict)
async def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
