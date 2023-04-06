from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "My User Management API"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    MAX_CONNECTIONS_COUNT = 10
    MIN_CONNECTIONS_COUNT = 10
    SECRET_KEY = "secret key for project"

    MONGODB_URL = "mongodb://localhost:27017"

    class Config:
        env_file = ".env"


settings = Settings()
