import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:root@db/arved"  # Docker Compose ühendus
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
