import logging
import os
from functools import lru_cache

from pydantic_settings import BaseSettings


IS_PRODUCTION = False
# TODO: Change the logger name to the appropriate name
LOGGER_NAME = os.getenv("LOGGER_NAME", "backend_base")

logger = logging.getLogger(LOGGER_NAME)


class Settings(BaseSettings):
    """
    This class defines the configuration settings for the application.

    Attributes:
        APP_NAME (str): The name of the application.
        APP_VERSION (str): The version of the application.
        MODE (str): The mode in which the application is running (e.g., development, production).
        LOG_LEVEL (int): The logging level for the application.
        SUMMARY (str): A brief summary of the application. Default is "Backend Base".

        ORIGINS (str): CORS allowed origins.
        ALLOWED_HOST (str): CORS allowed hosts.

        POSTGRES_HOST (str | None): The hostname for the PostgreSQL database.
        POSTGRES_USER (str | None): The username for the PostgreSQL database.
        POSTGRES_PASSWORD (str | None): The password for the PostgreSQL database.
        POSTGRES_DB (str | None): The database name for the PostgreSQL database.
        POSTGRES_PORT (str | None): The port for the PostgreSQL database.

        REDIS_URL (str): The URL for the Redis server.

        OPENAI_API_KEY (str): The API key for OpenAI.

        SENTRY_DSN (str): The DSN for Sentry error tracking.

    Config:
        extra (str): Configuration for handling extra fields. Default is "allow".
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

    SUMMARY: str = "Backend Base"

    #################################
    ###### CORS Config ##############
    #################################
    ORIGINS: str
    ALLOWED_HOST: str

    #################################
    ###### Database Config ##########
    #################################
    # Database type: 'sqlite' or 'postgresql'
    DATABASE_TYPE: str = "sqlite"
    # SQLite database file path (used when DATABASE_TYPE=sqlite)
    SQLITE_DB_PATH: str = "./db.sqlite3"
    # PostgreSQL configuration (used when DATABASE_TYPE=postgresql)
    POSTGRES_HOST: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: str | None = None
    POSTGRES_SCHEMA: str = "cv"

    #################################
    ###### REDIS Config ##########
    #################################
    REDIS_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    ###############################
    # OPEN AI
    ###############################
    OPENAI_API_KEY: str

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
    ###### sentry Config ############
    #################################
    SENTRY_DSN: str

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

    class Config:
        extra = "allow"


@lru_cache
def get_settings() -> Settings:
    """
    Retrieve and return the application settings.
    If not in production, load settings from a specific environment file.
    Returns:
        Settings: An instance of the Settings class containing
        application configurations.
    """
    if not IS_PRODUCTION:
        logger.info("Loading settings from .env file")
        return Settings(
            _env_file="./.env",
        )

    logger.debug("Loading settings from environment variables")
    return Settings()
