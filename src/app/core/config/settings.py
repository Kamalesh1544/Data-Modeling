import logging
from functools import lru_cache

from pydantic_settings import BaseSettings


IS_PRODUCTION = False
# TODO: Change the logger name to the appropriate name
LOGGER_NAME = "BACKEND_BASE"

logger = logging.getLogger(LOGGER_NAME)


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

    SUMMARY: str = "Backend Base"

    #################################
    ###### CORS Config ##############
    #################################
    ORIGINS: str
    ALLOWED_HOST: str

    #################################
    ###### Database Config ##########
    #################################
    POSTGRES_HOST: str | None
    POSTGRES_USER: str | None
    POSTGRES_PASSWORD: str | None
    POSTGRES_DB: str | None
    POSTGRES_PORT: str | None

    #################################
    ###### REDIS Config ##########
    #################################
    REDIS_URL: str
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

    ##############################################
    ################## NEO4J #####################
    ##############################################
    GRAPH_URL: str
    GRAPH_USER: str
    GRAPH_PASSWORD: str
    NEO4J_AUTH: str
    NEO4J_ACCEPT_LICENSE_AGREEMENT: str
    NEO4J_PLUGINS: list
    NEO4J_dbms_security_procedures_allowlist: str
    NEO4J_dbms_security_procedures_unrestricted: str
    NEO4J_server_memory_heap_initial__size: str
    NEO4J_server_memory_heap_max__size: str
    NEO4J_server_memory_pagecache_size: str
    NEO4J_apoc_export_file_enabled: bool

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


# create a single instance of the settings
# settings = Settings()
# logger = logging.getLogger(settings.MODE)


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
        return Settings(
            _env_file="./.env",
        )

    return Settings()
