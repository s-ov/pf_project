from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model

from .forms import TaskAssignmentForm
from users.models import Employee
from task.models import Task


def create_task_assignment_view(request):
    """Creates a new task assignment."""
    if request.method == 'POST':
        form = TaskAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workflow:task_doers_list') 
    else:
        form = TaskAssignmentForm()
    context = {
        'form': form,
        'title': 'Створи завдання',
        }
    return render(
        request, 
        'workflow/create_task_assignment.html', 
        context,
        )


def get_task_doers_view(request):
    """
    Displays a paginated list of Employee instances whose role is electricians. If an error occurs while
    fetching motors or pagination fails, the error is handled gracefully.
    
    Args:
        request (HttpRequest): The HTTP request object containing metadata 
                               about the request, including the 'page' query parameter.
    
    Returns:
        HttpResponse: The rendered 'doers_list.html' template displaying the paginated
                      list of doers and pagination controls, or an error message.
    """
    try:
        doers_list = Employee.objects.filter(role='Electrician').order_by('id')
        paginator = Paginator(doers_list, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    except (PageNotAnInteger, EmptyPage):  
        page_obj = paginator.page(1)

    except Employee.DoesNotExist:
        page_obj = None

    context = {
        'page_obj': page_obj,
        'title': 'Список електриків',
    }
    
    return render(request, 'workflow/doers_list.html', context)


def get_doer_tasks_view(request, doer_id):
    """View to list all tasks for a specific doer.
    
    Args: 
        request (HttpRequest): The HTTP request object containing metadata 
                               about the request, including the 'page' query parameter.
        doer_id (int): ID of requested doer.
    """
    try:
        doer = get_object_or_404(get_user_model(), id=doer_id)
    except Http404:
        return render(request, 'assignment/error_no_doer.html', {
            'message': 'Запит недійсний, тому що не існує такого електрика.',
            'title': 'Неіснуючий електрик',
        })

    tasks = Task.objects.filter(doer=doer)
    paginator = Paginator(tasks, 2)

    try:
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    context = {
        'page_obj': page_obj,
        'doer': doer,
        'title': f'Завдання для {doer.first_name} {doer.last_name}',
    }
    return render(request, 'workflow/doer_tasks_list.html', context)
