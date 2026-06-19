from pathlib import Path
from typing import Literal, Optional

from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'
APP_DIR = BASE_DIR / 'src'
STATIC_DIR = APP_DIR / 'static'


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, env_file_encoding='utf-8', extra='ignore'
    )



class AppConfig(ConfigBase):
    """
    Authentication and security settings for the application.

    Handles admin credentials and automated secret key generation
    using the 'APP_' environment prefix.
    """

    model_config = SettingsConfigDict(env_prefix='app_')
    mode: Literal['DEV', 'TEST', 'PROD']
    name: str = 'ToDo'
    logging_mode: str = 'on'
    admin_email: str
    admin_password: SecretStr



class AIConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix='ai_')
    api_key: str | None = None
    text_model: str | None = None
    speech_model: str | None = None


class Settings(BaseSettings):
    """
    Global application settings container.

    Integrates database connection and authentication configurations.
    """

    app_name: str = 'Todo'
    app: AppConfig = Field(default_factory=AppConfig)
    ai: AIConfig = Field(default_factory=AIConfig)

    @classmethod
    def load(cls) -> 'Settings':
        """Initializes and returns a Settings instance."""
        return cls()


settings: Settings = Settings.load()