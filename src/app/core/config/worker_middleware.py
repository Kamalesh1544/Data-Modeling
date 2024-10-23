from typing import Any

from taskiq import TaskiqMessage, TaskiqMiddleware, TaskiqResult

from src.app.core import logger


class MonitoringMiddleware(TaskiqMiddleware):
    def startup(self) -> None:
        logger.debug("RUNNING STARTUP")

    def shutdown(self) -> None:
        logger.debug("RUNNING SHUTDOWN")

    def pre_execute(self, message: "TaskiqMessage") -> TaskiqMessage:
        logger.info(f"PRE EXECUTE: {message.task_id}")
        return message

    def post_save(self, message: "TaskiqMessage", result: "TaskiqResult[Any]") -> None:
        logger.info(f"Saved Task: {message.task_id}")
        logger.debug(f"Result: {result.return_value}")

    def on_error(
        self,
        message: "TaskiqMessage",
        result: "TaskiqResult[Any]",
        exception: BaseException,
    ) -> None:
        logger.error(f"Exception on task: {message.task_id}", exc_info=exception)
        logger.error(
            f"Exception on task {message.task_id} Result: "
            f"{result.return_value if result else None}"
        )
