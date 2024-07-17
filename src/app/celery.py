from celery import Celery
from celery.result import AsyncResult

from src.app.core.config.settings import get_settings

settings = get_settings()
celery_app = Celery("app", broker=settings.CELERY_BROKER, backend=settings.CELERY_BACKEND)
celery_app.autodiscover_tasks()


# GET status about task info
def get_celery_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result
