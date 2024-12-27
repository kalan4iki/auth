from typing import Annotated, Literal

from fastapi import Form, HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRouter
from pony.orm import db_session

from db import User
from exception import AuthorizeException, AuthorizeTemplateException
from models import ErrorMessage
from models.token import RegisterRequest
from settings import TEMPLATES
from utils import clients, users, token
from utils.password import hash_password

auth_router = APIRouter(tags=["auth"])


# Эндпоинт для регистрации пользователя
@auth_router.post("/register", responses={401: {"model": ErrorMessage}})
async def register(data: RegisterRequest):
    with db_session:
        user = User.get(username=data.username)
        if user:
            raise HTTPException(
                status_code=400, detail={"message": "Username already exists"}
            )
        hashed_password = hash_password(data.password)
        User(username=data.username, hashed_password=hashed_password)
    return {"message": "User created successfully"}


# Форма для авторизации
@auth_router.get("/authorize")
async def authorize(
    request: Request,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
):
    # client = clients.get_client(client_id=client_id, redirect_uri=redirect_uri)
    return TEMPLATES.TemplateResponse(
        request=request,
        name="login.html",
        context=dict(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            state=state,
        ),
    )


@auth_router.post("/authorize")
async def authorize_post(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    client_id: Annotated[str, Form()],
    scope: Annotated[str, Form()],
    state: Annotated[str, Form()],
    redirect_uri: Annotated[str | None, Form()] = None,
    form: Annotated[Literal["form", "api"], Form()] = "form",
):
    try:
        # Блок получения клиента
        client = clients.get_client(client_id=client_id, redirect_uri=redirect_uri)

        # Блок получения пользователя
        user = users.get_user(username=username, password=password)
    except AuthorizeException as exc:
        if form == "form":
            raise AuthorizeTemplateException(detail=exc.detail)
        else:
            raise HTTPException(status_code=401, detail=exc.detail)
    code = token.create_authorization_code()
    url = f"{redirect_uri}{code}"
    if form == "form":
        if not redirect_uri:
            raise AuthorizeTemplateException(
                detail={"message": "Redirect url not found"}
            )
        return RedirectResponse(url=url)
    elif form == "api":
        return {
            "client_id": client_id,
            "scope": scope,
            "state": state,
            "authorization_code": code,
        }
