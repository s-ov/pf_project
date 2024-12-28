from django.test import TestCase
from django.utils.timezone import now, timedelta
from task.models import Task
from users.models import CustomUser
from task.tasks import reset_task_deadlines
import os

class ResetTaskDeadlinesTaskTest(TestCase):
    def setUp(self):
        "Create tasks with past, current, and future deadlines"
        self.user = CustomUser.objects.create_user(
            cell_number="+380964567890",
            first_name="John",
            last_name="Doe",
            password="securepassword123",
        )
        self.future_deadline_task = Task.objects.create(
            doer=self.user,
            task_description="Future Task",
            deadline=now() + timedelta(days=1),
            status=Task.TaskStatus.PENDING,
        )
        self.current_deadline_task = Task.objects.create(
            doer=self.user,
            task_description="Current Task",
            deadline=now(),
            status=Task.TaskStatus.IN_PROGRESS,
        )
        self.past_deadline_task = Task.objects.create(
            doer=self.user,
            task_description="Past Task",
            deadline=now() - timedelta(days=1),
            status=Task.TaskStatus.COMPLETED,
        )

        if os.path.exists('logs/task_deadline_update.log'):
            os.remove('logs/task_deadline_update.log')

    def test_task_resets_deadlines(self):
        """Test that the task resets deadlines for tasks with past or current deadlines."""
        result = reset_task_deadlines()

        self.future_deadline_task.refresh_from_db()
        self.current_deadline_task.refresh_from_db()

        self.assertIsNone(self.current_deadline_task.deadline)
        self.assertIsNotNone(self.past_deadline_task.deadline)

        self.assertIsNotNone(self.future_deadline_task.deadline)
        self.assertEqual(result, "Updated 1 tasks with past deadlines.")

    def tearDown(self):
        "Clean up the log file after tests"
        if os.path.exists('logs/task_deadline_update.log'):
            os.remove('logs/task_deadline_update.log')
