import os

MONGO_SETTINGS = {
    "host": os.getenv("DB_HOST", "piseiro-db"),
    "port": int(os.getenv("DB_PORT", "27017")),
    "db": os.getenv("DB_NAME", "piseiro"),
    "username": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "example"),
}

BROKER_URL = os.getenv("BROKER_URL", "amqp://guest:guest@rabbitmq:5672")

X_Y_FEED_RATE = int(os.getenv("X_Y_FEED_RATE", 2_000))

Z_FEED_RATE = int(os.getenv("Z_FEED_RATE", 1_000))

Z_BASE_DISTANCE = float(os.getenv("Z_BASE_DISTANCE", -139.5))

TO_CUT_OFFSET = float(os.getenv("TO_CUT_OFFSET", 0.5))

X_OFFSET = float(os.getenv("X_OFFSET", 4))

Y_OFFSET = float(os.getenv("Y_OFFSET", 4))
