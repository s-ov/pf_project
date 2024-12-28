from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from task.models import TaskArchive


class TaskArchiveModelTest(TestCase):
    def setUp(self):
        """Set up the test environment."""
        """Create a user to be linked to the TaskArchive model"""
        self.user = get_user_model().objects.create_user(
            cell_number='1234567890',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )

        self.task_archive = TaskArchive.objects.create(
            task_id=1,
            doer=self.user,
            task_description="Test task description",
            created_at=timezone.now(),
            deadline=timezone.now() + timezone.timedelta(days=1)
        )

    def test_task_archive_creation(self):
        """Test the creation of a TaskArchive instance."""
        self.assertEqual(self.task_archive.task_id, 1)
        self.assertEqual(self.task_archive.doer, self.user)
        self.assertEqual(self.task_archive.task_description, "Test task description")
        self.assertIsInstance(self.task_archive.created_at, timezone.datetime)
        self.assertIsInstance(self.task_archive.archived_at, timezone.datetime)

    def test_foreign_key_relationship(self):
        """Test the ForeignKey relationship to the user model."""
        self.assertEqual(self.task_archive.doer.cell_number, '1234567890')

    def test_archived_at_auto_add(self):
        """Test that 'archived_at' is set automatically."""
        self.assertIsNotNone(self.task_archive.archived_at)
        self.assertLess(self.task_archive.created_at, self.task_archive.archived_at)

    def test_task_archive_optional_deadline(self):
        """Test that the 'deadline' field is optional."""
        task_archive_no_deadline = TaskArchive.objects.create(
            task_id=2,
            doer=self.user,
            task_description="Another task description",
            created_at=timezone.now()
        )
        self.assertIsNone(task_archive_no_deadline.deadline)
