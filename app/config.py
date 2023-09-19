from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BROKER_URL: str = "amqp://test:test@rabbitmq:5672"
    BROKER_VHOST: str = "/"

    RABBITMQ_DEFAULT_USER: str = ""
    RABBITMQ_DEFAULT_PASS: str = "test"

    REGION_NAME: str = "us-east-1"
    ENDPOINT_URL: str = "http://dynamodb:4566"
    AWS_ACCESS_KEY_ID: str = "dummy12121"
    AWS_SECRET_ACCESS_KEY: str = "dummy12121"

    class Config:
        env_prefix = ''
        env_file = "app/.env"
        env_file_encoding = 'utf-8'


settings = Settings()

