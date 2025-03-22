from pydantic_settings import BaseSettings
from pyprojroot import here
import sys
sys.path.append(str(here()))

class Settings(BaseSettings):
    redis_host: str = "redis"
    mysql_host: str = "mysql"
    mysql_url: str = "mysql+asyncmy://appuser:apppass@mysql/appdb"
    cors_origins: list[str] = ["*"]

settings = Settings() 