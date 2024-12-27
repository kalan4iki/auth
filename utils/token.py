from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt
from pony.orm import db_session

from db import AccessToken, Client, User
from models.token import TokenData
from settings import setting


def create_authorization_code() -> str:
    """Функция создания кода авторизации

    :return: _description_
    :rtype: str
    """
    ...


def create_access_token(
    client: Client, user: User, data: dict, expires_delta: timedelta | None = None
) -> str:
    """Функция создания токена доступа

    :param client: _description_
    :type client: Client
    :param user: _description_
    :type user: User
    :param data: _description_
    :type data: dict
    :param expires_delta: _description_, defaults to None
    :type expires_delta: timedelta | None, optional
    :return: _description_
    :rtype: str
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    with db_session:
        AccessToken(user=user, client=client, access_token=encoded_jwt)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Функция верификации токена

    :param token: _description_
    :type token: str
    :raises HTTPException: _description_
    :raises HTTPException: _description_
    :return: _description_
    :rtype: TokenData
    """

    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data
