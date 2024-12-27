from .config import config_router
from .auth import auth_router
from .user import user_router


routers = [config_router, auth_router, user_router]