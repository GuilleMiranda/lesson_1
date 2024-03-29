from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    db_hostname: Optional[str]
    db_port: Optional[str]
    db_password: Optional[str]
    db_name: Optional[str]
    db_username: Optional[str]
    secret_key: Optional[str]
    algorithm: Optional[str]
    access_token_expiry_minutes: Optional[int]

    class Config:
        env_file = "/home/fastapi/.env"

settings = Settings()