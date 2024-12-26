from pony.orm import Database
from passlib.context import CryptContext

# База данных
db = Database()

# Контекст хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt")

def initialize_db():
    db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)
