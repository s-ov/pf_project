from django.urls import reverse
from .models import Employee


def employee_info(request):
    """
    Add user information to the context.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        dict: A dictionary containing the user information.
    """
    if request.user.is_authenticated:
        employee = None
        try:
            employee = Employee.objects.get(id=request.user.id)
            return {
            'employee_profile_url': reverse('users:employee_profile', kwargs={'employee_id': request.user.id}),
            'employee_logout_url': reverse('users:logout'),
            'employee': employee,
        }
        except Employee.DoesNotExist:
            employee = None  
    
    return {
        'employee_register_url': reverse('users:register'),
        'employee_login_url': reverse('users:login'),
    }
