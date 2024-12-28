from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model

from task.forms import StatusUpdateForm
from task.models import Task

class StatusUpdateFormTests(TestCase):
    def setUp(self):
        """Create a sample Task instance to use in tests"""
        self.task = Task.objects.create(
            doer=get_user_model().objects.create_user(
                cell_number='+380961020205', 
                password='testpassword',
                ),
            task_description="Test task",
            status=Task.TaskStatus.IN_PROGRESS,
            deadline=now() + timedelta(days=3),
        )

    def test_form_valid_data(self):
        """Test the form with valid data."""
        valid_deadline = now() + timedelta(hours=9)
        form_data = {
            'status': Task.TaskStatus.IN_PROGRESS,
            'deadline': valid_deadline.strftime('%Y-%m-%dT%H:%M:%S'), 
        }
        form = StatusUpdateForm(data=form_data, instance=self.task)
        print(form.errors)  
        self.assertTrue(form.is_valid(), "Form should be valid with proper data.")

    def test_form_invalid_deadline(self):
        """Test the form with an invalid deadline (less than one hour)."""
        invalid_deadline = now() + timedelta(minutes=30) 
        form_data = {
            'status': 'Completed',
            'deadline': invalid_deadline.strftime('%Y-%m-%dT%H:%M:%S'),  
        }
        form = StatusUpdateForm(data=form_data, instance=self.task)
        self.assertFalse(
            form.is_valid(), 
            "Form should be invalid with a deadline less than one hour later.",
            )
        self.assertIn(
            'deadline', 
            form.errors, "Deadline field should have validation errors.",
            )
        self.assertEqual(
            form.errors['deadline'][0],
            "Час закінчення має бути щонайменше на 1 годину пізніше часу створення завдання."
        )

    def test_form_invalid_status(self):
        """Test the form with an invalid status."""
        valid_deadline = now() + timedelta(hours=2)  
        form_data = {
            'status': 'InvalidStatus', 
            'deadline': valid_deadline.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        form = StatusUpdateForm(data=form_data, instance=self.task)
        self.assertFalse(
            form.is_valid(), 
            "Form should be invalid with an unrecognized status.",
            )
        self.assertIn(
            'status', 
            form.errors, "Status field should have validation errors.",
            )
