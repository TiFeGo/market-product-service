import enum
import os
from typing import Union

from pydantic import BaseSettings, Field
from dotenv import load_dotenv, dotenv_values

app_state = {
    'DEBUG': '.env-debug',
    'PRODUCTION': '.env-production',
    'DEVELOPMENT': '.env-development',
    'DEFAULT_ENV': '.env',
}


class Settings(BaseSettings):
    APP_ENV: str = 'debug'
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PORT: str

    TEST_DATABASE_NAME: str

    @classmethod
    def create(cls) -> 'Settings':
        app_env = os.getenv('APP_ENV', 'DEBUG')
        conf = dict(dotenv_values(app_state.get(app_env)))
        return Settings(**conf)


settings = Settings.create()
