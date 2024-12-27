from fastapi import Depends

from settings import oauth2_scheme
from utils.token import verify_token
from models.token import TokenData


def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Функция получения текущего пользователя

    :param token: _description_, defaults to Depends(oauth2_scheme)
    :type token: str, optional
    :return: _description_
    :rtype: TokenData
    """
    return verify_token(token)
