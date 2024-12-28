from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from twilio.rest import Client

from .models import Task, TaskArchive


@receiver(post_save, sender=Task)
def archive_completed_task(sender, instance, **kwargs):
    """
    Archive a task when its status is set to COMPLETED.
    """
    if instance.status == Task.TaskStatus.COMPLETED:
        print(f"Signal triggered for Task ID: {instance.id}, Status: {instance.status}")
        TaskArchive.objects.create(
            task_id=instance.id,
            doer=instance.doer,
            task_description=instance.task_description,
            created_at=instance.created_at,
            deadline=instance.deadline,
        )

        if not hasattr(instance, '_is_archived'):
            instance._is_archived = True
            instance.delete()
