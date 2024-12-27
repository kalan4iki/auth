from pony.orm import db_session

from db import Client
from exception import AuthorizeException


def get_client(client_id: str, redirect_uri: str, client_secret: str | None = None, secret_check: bool = False) -> Client:
    with db_session:
        client = Client.get(client_id=client_id)
        if not client:
            raise AuthorizeException(
                detail={"message": "Invalid client ID"}
            )
        if client.client_secret != client_secret and secret_check:
            raise AuthorizeException(
                detail={"message": "Invalid client secret"}
            )
        # TODO: Добавить проверку адреса перехода

    return client
