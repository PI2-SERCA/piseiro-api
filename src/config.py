import os

MONGO_SETTINGS = {
    "host": "piseiro-db",
    "port": 27017,
    "db": os.getenv("DB_NAME", "piseiro"),
    "username": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "example"),
}
