from django.db import models
from work_tower.models.node import Node


class TaskAssignment(models.Model):
    """Represents the task assignment linking Task and Node instances."""
    task = models.ForeignKey(
        'task.Task', 
        on_delete=models.CASCADE, 
        related_name='assignments',
        )
    node = models.ForeignKey(
        Node, 
        on_delete=models.CASCADE, 
        related_name='assignments', 
        null=True, blank=True,
        )

