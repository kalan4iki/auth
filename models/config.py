from pydantic import BaseModel


class ApiConfiguration(BaseModel):
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str


class KeyModel(BaseModel):
    kty: str
    n: str
    e: str
    kid: str


class JWKSResponse(BaseModel):
    keys: list[KeyModel]
