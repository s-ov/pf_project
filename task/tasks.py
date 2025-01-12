from celery import shared_task
from task.management.commands.reset_deadlines import reset_deadlines


@shared_task
def run_management_command():
    """Celery task to reset deadlines for overdue tasks."""
    updated_count = reset_deadlines()
    return f"Updated {updated_count} tasks."
    

run_management_command.apply_async(retry=True, countdown=60)
