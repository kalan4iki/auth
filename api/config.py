from fastapi.routing import APIRouter

from utils import get_url
from utils.keys import get_key

config_router = APIRouter(prefix="/.well-known", tags=["config"])


# Эндпоинт для конфигурации OpenID Connect
@config_router.get("/openid-configuration")
async def openid_configuration():
    base_url = get_url()
    return {
        "issuer": base_url,
        "authorization_endpoint": base_url + "/user/authorize",
        "token_endpoint": base_url + "/user/token",
        "userinfo_endpoint": base_url + "/user/userinfo",
        "jwks_uri": base_url + "/.well-known/jwks.json",
    }


# Эндпоинт для набора открытых ключей
@config_router.get("/jwks.json")
async def jwks():
    public_key = get_key("public", False)
    return {
        "keys": [
            {
                "kty": "RSA",
                "n": public_key.public_numbers().n.to_bytes(256, byteorder="big").hex(),
                "e": public_key.public_numbers().e.to_bytes(3, byteorder="big").hex(),
                "kid": "general",
            }
        ]
    }
