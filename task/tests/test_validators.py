from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError
from task.validators import validate_minimum_one_hour_later


class ValidateMinimumOneHourLaterTests(TestCase):
    
    def test_valid_deadline_one_hour_later(self):
        """Test that a deadline exactly one hour later is valid."""
        reference_time = now()
        valid_deadline = reference_time + timedelta(hours=1)
        try:
            validate_minimum_one_hour_later(valid_deadline, reference_time=reference_time)
        except ValidationError:
            self.fail("validate_minimum_one_hour_later() raised ValidationError unexpectedly!")

    def test_valid_deadline_more_than_one_hour_later(self):
        """Test that a deadline more than one hour later is valid."""
        valid_deadline = now() + timedelta(hours=2)
        try:
            validate_minimum_one_hour_later(valid_deadline)
        except ValidationError:
            self.fail("validate_minimum_one_hour_later() raised ValidationError unexpectedly!")

    def test_invalid_deadline_less_than_one_hour_later(self):
        """Test that a deadline less than one hour later raises ValidationError."""
        invalid_deadline = now() + timedelta(minutes=59)
        with self.assertRaises(ValidationError) as context:
            validate_minimum_one_hour_later(invalid_deadline)
        self.assertEqual(
            str(context.exception.message),
            "Час закінчення має бути щонайменше на 1 годину пізніше часу створення завдання.",
        )

    def test_invalid_deadline_in_the_past(self):
        """Test that a past deadline raises ValidationError."""
        invalid_deadline = now() - timedelta(hours=1)
        with self.assertRaises(ValidationError) as context:
            validate_minimum_one_hour_later(invalid_deadline)
        self.assertEqual(
            str(context.exception.message),
            "Час закінчення має бути щонайменше на 1 годину пізніше часу створення завдання.",
        )
    