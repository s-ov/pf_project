from django.test import TestCase
from django.db.models.signals import post_save
from task.models import Task, TaskArchive
from django.contrib.auth import get_user_model


class ArchiveCompletedTaskSignalTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            cell_number='+380964567890',
            password='password123',
            first_name='John',
            last_name='Doe',
        )
        self.task = Task.objects.create(
            doer=self.user,
            task_description="Complete the wiring",
            status=Task.TaskStatus.PENDING,
            created_at="2024-12-20 10:00:00",
            deadline="2024-12-30 10:00:00",
        )

    def test_task_deleted_after_archiving(self):
        """Test that the original Task instance is deleted after being archived."""
        self.task.status = Task.TaskStatus.COMPLETED
        self.task.save()

        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)

    def test_no_action_when_status_not_completed(self):
        """Test that no TaskArchive instance is created if the Task status is not COMPLETED."""
        self.task.status = Task.TaskStatus.IN_PROGRESS
        self.task.save()

        self.assertFalse(TaskArchive.objects.filter(task_id=self.task.id).exists())
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
