from pony.orm import Required

from .base import db
from .client import Client
from .user import User


# Модель кода авторизации
class AuthorizationCode(db.Entity):
    code = Required(str, unique=True)
    user = Required(User)
    client = Required(Client)


# Модель токена доступа
class AccessToken(db.Entity):
    access_token = Required(str, unique=True)
    user = Required(User)
    client = Required(Client)
