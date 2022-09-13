import os

MONGO_SETTINGS = {
    "host": os.getenv("DB_HOST", "piseiro-db"),
    "port": os.getenv("DB_PORT", "27017"),
    "db": os.getenv("DB_NAME", "piseiro"),
    "username": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "example"),
}
