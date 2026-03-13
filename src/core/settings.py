import enum
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Enviroments(enum.IntEnum):
    DEV = 1
    TESTING = 2
    PROD = 3

    @classmethod
    def from_str(cls, value: Union[str, int]) -> 'Enviroments':
        if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
            return cls(int(value))
        value_map = {
            'DEV': cls.DEV,
            'TESTING': cls.TESTING,
            'PROD': cls.PROD
        }
        return value_map[value.upper()]

class Settings(BaseSettings):
    ENV: Enviroments
    TELEGRAM_TOKEN: str = "6501714435:AAE-jHFRvn9Pn4N1UIW12mD0mujT0h4jrFQ"
    ADMINISTRATOR_IDS: list = ["1704946509"]
  
    PROJECT_FLAG: str = "Project: Investment Memo Engine"
    
    # OpenAI configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Server configuration
    host: str = "127.0.0.1"
    port: int = 8080

    @field_validator('ENV', mode='before')
    @classmethod
    def validate_env(cls, value):
        if value is None:
            return Enviroments.DEV
        try:
            return Enviroments.from_str(value)
        except (KeyError, ValueError):
            return Enviroments.DEV

class DevelopmentSettings(Settings):
    ENV: Enviroments = Enviroments.DEV

    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        extra="allow",
        env_nested_delimiter="__",
        case_sensitive=False
    )

class TestingSettings(Settings):
    ENV: Enviroments = Enviroments.TESTING

    model_config = SettingsConfigDict(
        env_file=".env.test",
        env_file_encoding="utf-8",
        extra="allow",
        env_nested_delimiter="__",
        case_sensitive=False
    )

class ProductionSettings(Settings):
    ENV: Enviroments = Enviroments.PROD

    model_config = SettingsConfigDict(
        env_file=".env.prod",
        env_file_encoding="utf-8",
        extra="allow",
        env_nested_delimiter="__",
        case_sensitive=False
    )