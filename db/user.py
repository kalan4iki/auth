from pony.orm import PrimaryKey, Required, Set

from .base import db
from utils.password import verify_password, hash_password


# Модель пользователя
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    hashed_password = Required(str)
    codes = Set("AuthorizationCode")
    tokens = Set("AccessToken")

    def set_password(self, password: str):
        self.hashed_password = hash_password(password)

    def check_password(self, provided_password: str) -> bool:
        return verify_password(self.hashed_password, provided_password)
