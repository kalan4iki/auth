from fastapi import Depends, HTTPException

from settings import oauth2_scheme
from utils.token import verify_token


# Функция получения текущего пользователя
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
