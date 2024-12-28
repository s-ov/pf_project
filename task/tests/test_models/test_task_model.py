from django.test import TestCase
from django.utils.timezone import now, timedelta, datetime, timezone
from task.models import Task
from users.models import CustomUser

class TaskModelTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.user = CustomUser.objects.create_user(
            cell_number="1234567890",
            first_name="John",
            last_name="Doe",
            password="securepassword123",
        )
        self.task = Task.objects.create(
            doer=self.user,
            task_description="Test task description",
            deadline=now() + timedelta(hours=2),
            status=Task.TaskStatus.IN_PROGRESS,
        )

    def test_task_default_status(self):
        """Test the default status is set to IN_PROGRESS."""
        task = Task.objects.create(doer=self.user, task_description="Another task")
        self.assertEqual(task.status, Task.TaskStatus.IN_PROGRESS)

    def test_check_deadline_validity_with_valid_deadline(self):
        """Test that `check_deadline_validity` does not change a valid deadline."""
        initial_deadline = self.task.deadline
        self.task.check_deadline_validity()
        self.assertEqual(self.task.deadline, initial_deadline)

    def test_check_deadline_validity_with_past_deadline(self):
        """Test that `check_deadline_validity` sets deadline to None for past deadlines."""
        self.task.deadline = now() - timedelta(hours=1)
        self.task.save()
        self.task.check_deadline_validity()
        self.assertIsNone(self.task.deadline)

    def test_check_deadline_validity_with_current_time_deadline(self):
        """Test that `check_deadline_validity` sets deadline to None for deadlines at current time."""
        self.task.deadline = datetime.now(timezone.utc)
        self.task.save()
        self.task.check_deadline_validity()
        self.assertIsNone(self.task.deadline)
