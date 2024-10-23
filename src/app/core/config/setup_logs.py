import logging
import sys

from fastapi.logger import logger as fastapi_logger


def init_logger(level):
    """
    Initialize loggers for different components with the
    specified logging level.

    Args:
    - level: The logging level to set for all loggers.

    Components initialized:
    - gunicorn_error_logger: Logger for gunicorn errors.
    - uvicorn_access_logger: Logger for uvicorn access.
    - fastapi_logger: Logger for FastAPI.
    - logger_db_client: Logger for database client.
    - logger_tortoise: Logger for Tortoise ORM.
    """
    # GCLOUD SETUP
    # client = Client()
    # client.get_default_handler()
    # client.setup_logging()

    # setup logging
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    # gunicorn_logger = logging.getLogger("gunicorn")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.setLevel(level)

    # will print debug sql
    logger_db_client = logging.getLogger("db_client")
    logger_db_client.setLevel(level)
    logger_db_client.addHandler(fastapi_logger)

    logger_tortoise = logging.getLogger("tortoise")
    logger_tortoise.setLevel(level)
    logger_tortoise.addHandler(fastapi_logger)

    # register custom logger here
    injector_logging = logging.getLogger("injector")
    injector_logging.setLevel(logging.DEBUG)
    injector_logging.addHandler(fastapi_logger)

    # Register custom logger for coding
    # TODO: Change the logger name to the appropriate name
    backend_logging = logging.getLogger("BACKEND_BASE")
    backend_logging.setLevel(logging.DEBUG)
    backend_logging.addHandler(fastapi_logger)

    # Package logger
    package_logger = logging.getLogger("PACKAGE")
    package_logger.setLevel(level)
    package_logger.addHandler(fastapi_logger)

    # Create console handler and set level to DEBUG
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    )
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    # Add console handler to logger
    fastapi_logger.addHandler(console_handler)
