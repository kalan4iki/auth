import secrets
from datetime import datetime, timedelta

from jose import JWTError, jwt
from pony.orm import db_session

from db import AuthorizationCode, AccessToken
from models.token import TokenData
from settings import setting


def create_authorization_code(user, client):
    code = secrets.token_urlsafe(16)
    # Храним код авторизации в базе данных
    with db_session:
        AuthorizationCode(code=code, user=user, client=client)
    return code


# Функция создания токена доступа
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return encoded_jwt


# Функция верификации токена
def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data
