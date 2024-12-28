from django.test import TestCase
from django.utils.timezone import now, timedelta
from task.models import Task
from django.core.management import call_command
from django.conf import settings
from users.models import CustomUser


class SetDeadlineToNullCommandTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            cell_number="1234567890",
            first_name="John",
            last_name="Doe",
            password="securepassword123",
        )
        self.future_deadline_task = Task.objects.create(
            doer=self.user,
            task_description="Future task",
            deadline=now() + timedelta(days=1),
            status=Task.TaskStatus.PENDING,
        )
        self.current_deadline_task = Task.objects.create(
            doer=self.user,
            task_description="Current task",
            deadline=now(),
            status=Task.TaskStatus.IN_PROGRESS,
        )
        self.past_deadline_task = Task.objects.create(
            doer=self.user,
            task_description="Past task",
            deadline=now() - timedelta(days=1),
            status=Task.TaskStatus.COMPLETED,
        )

    def test_command_updates_deadlines(self):
        """
        Test that the command sets deadlines to NULL 
        for tasks with past or current deadlines.
"""
        call_command('reset_deadlines')
        self.future_deadline_task.refresh_from_db()
        self.current_deadline_task.refresh_from_db()

        self.assertIsNone(self.current_deadline_task.deadline)
        self.assertIsNotNone(self.past_deadline_task.deadline)
        self.assertIsNotNone(self.future_deadline_task.deadline)
