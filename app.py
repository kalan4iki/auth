from fastapi import FastAPI
from fastapi.requests import Request

from db import initialize_db
from exception import AuthorizeTemplateException
from settings import TEMPLATES
from utils.keys import check_keys_file_exists
from api import routers

# Приложение
app = FastAPI()


# Функции инициализации
check_keys_file_exists()
initialize_db()

for i in routers:
    app.include_router(i)



@app.exception_handler(AuthorizeTemplateException)
async def authorize_exception_handler(
    request: Request, exc: AuthorizeTemplateException
):
    return TEMPLATES.TemplateResponse(
        request=request, name="login_error.html", context={"detail": exc.detail}
    )
