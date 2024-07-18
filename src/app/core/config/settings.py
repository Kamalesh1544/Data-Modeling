from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings

IS_PRODUCTION = False
LOGGER_NAME = "exception"


class Settings(BaseSettings):
    """
        Define settings for the application including app name, 
        version, mode, log level, CORS configuration, database configuration, 
        Redis configuration, email configuration, and Celery configuration.
    """
    APP_NAME: str
    APP_VERSION: str
    MODE: str
    # CRITICAL = 50
    # FATAL = CRITICAL
    # ERROR = 40
    # WARNING = 30
    # WARN = WARNING
    # INFO = 20
    # DEBUG = 10
    # NOTSET = 0
    LOG_LEVEL: int

    SUMMARY: str = "User Management API"

    #################################
    ###### CORS Config ##############
    #################################
    ORIGINS: str
    ALLOWED_HOST: str

    #################################
    ###### Database Config ##########
    #################################
    POSTGRES_HOST: Optional[str]
    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: Optional[str]
    POSTGRES_PORT: Optional[str]

    #################################
    ###### REDIS Config ##########
    #################################
    REDIS_URL: str

    #################################
    ###### EMAIL Config ##########
    #################################
    # MAIL_USERNAME: str
    # MAIL_PASSWORD: str
    # MAIL_FROM: str
    # MAIL_PORT: int
    # MAIL_SERVER: str
    # MAIL_TLS: bool
    # MAIL_SSL: bool
    # USE_CREDENTIALS: bool

    #################################
    ###### Celery Config ############
    #################################
    CELERY_BROKER: str
    CELERY_BACKEND: str

    # Create Email Config
    # using FastAPI Mail
    # def email_config(self) -> ConnectionConfig:
    #     return ConnectionConfig(
    #         MAIL_USERNAME=self.MAIL_USERNAME,
    #         MAIL_PASSWORD=self.MAIL_PASSWORD,
    #         MAIL_FROM=self.MAIL_FROM,
    #         MAIL_PORT=self.MAIL_PORT,
    #         MAIL_SERVER=self.MAIL_SERVER,
    #         MAIL_TLS=self.MAIL_TLS,
    #         MAIL_SSL=self.MAIL_SSL,
    #         USE_CREDENTIALS=self.USE_CREDENTIALS
    #     )


# create a single instance of the settings
# settings = Settings()
# logger = logging.getLogger(settings.MODE)

@lru_cache()
def get_settings() -> Settings:
    """
    Retrieve and return the application settings.
    If not in production, load settings from a specific environment file.
    Returns:
        Settings: An instance of the Settings class containing application configurations.
    """
    if not IS_PRODUCTION:
        return Settings(_env_file='/home/shudipto/PycharmProjects/Fastapi-Starter/.env')

    return Settings()