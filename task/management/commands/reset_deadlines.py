from django.core.management.base import BaseCommand
from task.models import Task
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
handler = logging.FileHandler('logs/task_deadline_update.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def reset_deadlines():
    """Set deadline to NULL for tasks with past or current deadlines."""
    now = datetime.now(timezone.utc)
    tasks_to_update = Task.objects.filter(deadline__lte=now)

    updated_count = 0
    for task in tasks_to_update:
        task.deadline = None
        task.save()
        updated_count += 1

    logger.info(f"Total uncompleted tasks: {updated_count}")
    return updated_count


class Command(BaseCommand):
    help = "Set deadline to NULL for tasks with past or current deadlines"

    def handle(self, *args, **kwargs):
        updated_count = reset_deadlines()
        self.stdout.write(self.style.SUCCESS(
            f"Updated {updated_count} tasks with past deadlines.",
            )
        )



# class Command(BaseCommand):
#     help = "Set deadline to NULL for tasks with past or current deadlines"

#     def handle(self, *args, **kwargs):
#         now = datetime.now(timezone.utc)
#         tasks_to_update = Task.objects.filter(deadline__lte=now)

#         updated_count = 0
#         for task in tasks_to_update:
#             task.deadline = None
#             task.save()
#             updated_count += 1

#         logger.info(f"Total uncompleted tasks: {updated_count}")
#         self.stdout.write(self.style.SUCCESS(f"Updated {updated_count} tasks with past deadlines."))
