import logging

from fastapi.logger import logger as fastapi_logger


def init_logger(level):
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
