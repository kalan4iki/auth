from pony.orm import PrimaryKey, Required, Set

from .base import db, pwd_context


# Модель пользователя
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    hashed_password = Required(str)
    codes = Set("AuthorizationCode")
    tokens = Set("AccessToken")

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)
