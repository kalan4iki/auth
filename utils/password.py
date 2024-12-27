from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

# Создание экземпляра хешировщика паролей
ph = PasswordHasher()


# Хеширование пароля
def hash_password(password: str) -> str:
    return ph.hash(password)


# Проверка хешированного пароля
def verify_password(hashed_password: str, provided_password: str) -> bool:
    try:
        return ph.verify(hashed_password, provided_password)
    except VerificationError:
        return False
