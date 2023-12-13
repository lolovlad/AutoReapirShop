from pydantic_settings import BaseSettings


class Config(BaseSettings):
    pg_user: str
    pg_password: str
    pg_db: str
    pg_port: int
    pg_host: str


settings = Config(_env_file='.env', _env_file_encoding='utf-8')
