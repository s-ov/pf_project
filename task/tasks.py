from celery import shared_task
from task.management.commands.reset_deadlines import reset_deadlines


@shared_task
def reset_deadlines_task():
    """Celery task to reset deadlines for overdue tasks."""
    updated_count = reset_deadlines()
    return f"Updated {updated_count} tasks."
    