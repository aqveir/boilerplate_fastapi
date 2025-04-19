import os
from typing import List

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8080
    WRITER_DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    READER_DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"

    # AWS settings
    AWS_ACCESS_KEY_ID: str = "AKIAUSRZADENQ6Z5S3EU"
    AWS_SECRET_ACCESS_KEY: str = "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"
    AWS_REGION: str = "us-east-1"

    AWS_S3_ENDPOINT_URL: str = "https://s3.amazonaws.com"
    AWS_S3_REGION_NAME: str = "us-east-1"
    AWS_S3_BUCKET: str = ""

    # JWT settings
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES: int = 3600
    JWT_ISSUER: str = "fastapi"
    JWT_AUDIENCE: str = "fastapi"

    # Auth settings
    CLAIM_STORAGE: str = "dynamodb"
    CLAIM_TABLE_NAME: str = "auth_claim_table"
    CLAIM_TABLE_KEY: str = "key"

    # Domain settings
    RESTRICTED_DOMAINS: list[str] = ["example.com", "gmail.com"]
    ALLOWED_DOMAINS: list[str] = [
        "localhost",
        "aqveir.in",
        "*.aqveir.in",
    ]

    SENTRY_SDN: str = ""
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class TestConfig(Config):
    DEBUG: bool = False
    # WRITER_DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi_test"
    # READER_DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi_test"


class LocalConfig(Config):
    ...


class ProductionConfig(Config):
    ENV: str = "production"
    DEBUG: bool = False


def get_config() -> Config:
    env = os.getenv("ENV", "local")
    config_type: List[str, Config] = {
        "local": LocalConfig(),
        "test": TestConfig(),
        "production": ProductionConfig(),
    }
    return config_type[env].model_validate({})


config: Config = get_config()
