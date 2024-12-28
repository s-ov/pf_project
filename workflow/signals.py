import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
 
from twilio.rest import Client
from django.conf import settings

from task.models import Task
from users.models import Employee 


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Task)
def send_task_sms_notification(sender, instance, created, **kwargs):
    """
    Signal that triggers sending sms to a certain user 
    after a Task for him has been created.
    
    Args:
        sender: The model class (Task).
        instance: The actual instance being saved (the Task instance).
        created: Boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.
    """
    
    if created:
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = f"{instance.task_description}. Закінчити до {instance.deadline}."

            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=instance.doer.cell_number
            )
            logger.info(f"Sending SMS to {instance.doer.cell_number}\
                          from {settings.TWILIO_PHONE_NUMBER}")
            print(f"Sending SMS to {instance.doer.cell_number}\
                    from {settings.TWILIO_PHONE_NUMBER}")
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")
            print(f"Помилка відправки SMS: {e}")
