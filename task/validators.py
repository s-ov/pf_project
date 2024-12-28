from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError

def validate_minimum_one_hour_later(value, reference_time=None):
    """
    Validates that the given datetime is at least one hour later than the reference time.

    Args:
        value (datetime): The datetime value to validate.
        reference_time (datetime): The reference datetime to compare against. Defaults to now().

    Raises:
        ValidationError: If the value is less than or equal to one hour later than the reference time.
    """
    if reference_time is None:
        reference_time = now()
    minimum_allowed_time = reference_time + timedelta(hours=1)
    if value < minimum_allowed_time:
        raise ValidationError(
            "Час закінчення має бути щонайменше на 1 годину пізніше часу створення завдання.",
        )
