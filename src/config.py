from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str
    debug: bool

    # Database
    database_url: str

    # CRPT Proxy
    timeout_seconds: int

    # Server
    host: str
    port: int

    # SSL
    ssl_keyfile: Optional[str] = None
    ssl_certfile: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
