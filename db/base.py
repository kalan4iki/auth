from pony.orm import Database

# База данных
db = Database()


def initialize_db():
    db.bind(provider="sqlite", filename="database.sqlite", create_db=True)
    db.generate_mapping(create_tables=True)
