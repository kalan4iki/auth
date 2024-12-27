from pony.orm import db_session

from db import User
from exception import AuthorizeException


def get_user(username: str, password: str) -> User:
    with db_session:
        user = User.get(username=username)
        if not user:
            raise AuthorizeException(
                status_code=401, detail={"message": "Incorrect username or password"}
            )
        if not user.verify_password(password):
            raise AuthorizeException(
                status_code=401, detail={"message": "Incorrect username or password"}
            )
