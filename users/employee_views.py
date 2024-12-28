from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

from .models import Employee
from .employee_forms import (
    EmployeeRegistrationForm, 
    EmployeeAdmissionGroupUpdateForm,
    )


def employee_register_view(request):
    """ Handle user registration.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the registration form on GET request.
                      Redirects to login page on successful POST request.
    """
    
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.set_password(form.cleaned_data['password'])
            employee.save()
            return redirect('users:login') 
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'users/registration/register.html', {'form': form})


# @login_required
def employee_profile_view(request, employee_id):
    """ Render the user profile page for a specific user based on user ID.

    Args:
    - request: HttpRequest object representing the request made to the view.
    - employee_id: ID of the user whose profile is being viewed.

    Returns:
    - HttpResponse object rendering the 'users/user_profile.html' template with user data.

    Raises:
    - Http404: If no user with the specified cell number exists in the database.
    """
    try:
        employee = get_object_or_404(Employee, id=employee_id)
    except Http404:
        return render(request, 'users/404.html', {'title': "Такого користувача не знайдено."})
    return render(
        request, 
        'users/employee_profile.html', {'employees': [employee], 'title': 'Мій профіль'})


def get_electricians_view(request):
    """ Get all employee which role is electrician

    Args:
    request (HttpRequest): The HTTP request object containing metadata about the request.
    
    Returns:
        HttpResponse: The rendered 'electricians_list.html' template displaying the paginated
                      list of users whose role is electrician and pagination control.
    """
    try:
        electricians_list = Employee.objects.filter(role='Electrician').order_by('id')
        paginator = Paginator(electricians_list, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except (PageNotAnInteger, EmptyPage):  
        page_obj = paginator.page(1)

    except Employee.DoesNotExist:
        page_obj = None

    context = {
        'electricians': electricians_list,
        'page_obj': page_obj,
        'title': 'Список електриків',
    }
    
    return render(request, 'users/electricians_list.html', context)
    

def update_employee_admission_group_view(request, employee_id):
    """
    View to update the admission group of an employee.

    Args:
        request (HttpRequest): The request object.
        employee_id (int): The ID of the employee to update.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    
    if employee.role != Employee.Role.ELECTRICIAN:
        messages.error(request, "Група допуску може бути оновлена тільки для електрика.")
        return redirect('users:electricians_list')

    if request.method == 'POST':
        form = EmployeeAdmissionGroupUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f"Група допуску для {employee.first_name} {employee.last_name} оновлена.")
            return redirect('users:electricians_list')
        else:
            messages.error(request, "Виправте помилки нижче.")
    else:
        form = EmployeeAdmissionGroupUpdateForm(instance=employee)

    return render(request, 'users/employee_update_form.html', {
        'form': form,
        'employee': employee,
        'title': 'Група допуску',
    })
