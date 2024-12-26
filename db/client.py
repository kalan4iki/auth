from pony.orm import PrimaryKey, Required, Set

from .base import db


# Модель клиента
class Client(db.Entity):
    id = PrimaryKey(int, auto=True)
    client_id = Required(str, unique=True)
    client_secret = Required(str)
    redirect_urls = Set("UrlRedirect")
    codes = Set("AuthorizationCode")
    tokens = Set("AccessToken")
    scope = Required(str)


# Модель адреса перенаправления
class UrlRedirect(db.Entity):
    id = PrimaryKey(int, auto=True)
    url = Required(str)
    client = Required(Client)
