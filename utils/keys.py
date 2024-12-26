import os
from typing import Literal, TypedDict

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
    generate_private_key,
)

from settings import BASE_DIR


class KeyPair(TypedDict):
    private: RSAPrivateKey
    public: RSAPublicKey


class KeyPemPairs(TypedDict):
    private: bytes
    public: bytes


def generate_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    # Генерация приватного ключа
    private_key = generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )

    # Генерация открытого ключа
    public_key = private_key.public_key()
    return private_key, public_key


def save_keys_to_file(private_key: RSAPrivateKey, public_key: RSAPublicKey):
    # Серилизация приватного ключа
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Серилизация открытого ключа
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Создание директории keys, если её нет
    if not os.path.exists(BASE_DIR / "keys"):
        os.makedirs(BASE_DIR / "keys")

    # Сохранение сериализованных ключей в файлы.pem
    with open(BASE_DIR / "keys" / "private_key.pem", "wb") as f:
        f.write(private_key_pem)

    with open(BASE_DIR / "keys" / "public_key.pem", "wb") as f:
        f.write(public_key_pem)


def check_keys_file_exists():
    if (
        not os.path.exists(BASE_DIR / "keys")
        or not os.path.exists(BASE_DIR / "keys/private_key.pem")
        or not os.path.exists(BASE_DIR / "keys/public_key.pem")
    ):
        private_key, public_key = generate_keys()
        save_keys_to_file(private_key, public_key)


def get_key(type_key: Literal["private", "public"], pem: bool = True) -> bytes | RSAPrivateKey | RSAPublicKey:
    check_keys_file_exists()
    key = None
    if type_key == "private":
        with open(BASE_DIR / "keys" / "private_key.pem", "rb") as f:
            key = f.read()
    elif type_key == "public":
        with open(BASE_DIR / "keys" / "public_key.pem", "rb") as f:
            key = f.read()
    if pem:
        return key
    else:
        if type_key == "private":
            return serialization.load_pem_private_key(key, password=None)
        elif type_key == "public":
            return serialization.load_pem_public_key(key)
