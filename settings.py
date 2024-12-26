from pathlib import Path
import secrets
from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DOMAIN: str = "127.0.0.1:8000"
    SSL: bool = True


setting = Settings()



# OAuth2 схема
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


BASE_DIR = Path(__file__).resolve().parent

if not setting.SECRET_KEY:
    path_key = BASE_DIR / "keys" / "secret_key"
    key = None
    if not os.path.exists(path_key):
        key = secrets.token_urlsafe(24)
        with open(path_key, "w") as f:
            f.write(key)
    else:
        with open(path_key, "r") as f:
            key = f.read()
    setting.SECRET_KEY = key