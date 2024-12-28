from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from datetime import datetime, timezone


class Task(models.Model):
    """The model describes servicing instance"""

    class TaskStatus(models.TextChoices):
        PENDING = 'PE', _('Призупинено')
        IN_PROGRESS = 'IP', _('На виконанні')
        COMPLETED = 'CO', _('Закінчено')
        CANCELED = 'CE', _('Скасовано')

    doer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    task_description = models.TextField(default="Завдання не поставлено.")
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(
        blank=True, 
        null=True, 
    )
    status = models.CharField(
        max_length=2,
        choices=TaskStatus.choices,
        default=TaskStatus.IN_PROGRESS
    )

    class Meta:
        ordering = ['-created_at'] 
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return f'Завдання N{self.id}: {self.task_description}'
    
    def check_deadline_validity(self):
        """Set deadline to null if it's past or equal to the current time."""
        if self.deadline and self.deadline < datetime.now(timezone.utc):
            self.deadline = None
            self.save()


class TaskArchive(models.Model):
    """Archived Task model."""
    task_id = models.IntegerField()  
    doer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='archived_tasks'
    )
    task_description = models.TextField()
    created_at = models.DateTimeField()
    deadline = models.DateTimeField(blank=True, null=True)
    archived_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Task N{self.task_id} archived at {str(self.archived_at)[:19]}"

