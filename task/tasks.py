# from celery import shared_task
# from task.models import Task
# from datetime import datetime, timezone
# import logging

# logger = logging.getLogger(__name__)
# handler = logging.FileHandler('logs/task_deadline_update.log')  
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)


# @shared_task
# def reset_task_deadlines():
#     now = datetime.now(timezone.utc)
#     tasks_to_update = Task.objects.filter(deadline__lte=now)

#     updated_count = 0
#     for task in tasks_to_update:
#         task.deadline = None
#         task.save()
#         updated_count += 1

#     logger.info(f"Total uncompleted tasks: {updated_count}")
#     return f"Updated {updated_count} tasks with past deadlines."
