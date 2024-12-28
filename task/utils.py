from django.shortcuts import render
from .models import Task


def task_update_message(request, status):
    """Redirect to an appropriate after status updating

    Args:
        - status (Task.TaskStatus): status of a specific Task

    Returns:
        - HttpResponse: Renders HttpResponse
    """
    
    if status == Task.TaskStatus.CANCELED:
        return render(
            request,
            'task/messages/canceled_status.html',
            {'title': 'Статус завдання'},
        )
    elif status == Task.TaskStatus.COMPLETED:
        return render(
            request,
            'task/messages/completed_status.html',
            {'title': 'Завдання закінчено'},
        )
    elif status == Task.TaskStatus.PENDING:
        return render(
            request,
            'task/messages/pending_status.html',
            {'title': 'Завдання відкладено'},
        )
    elif status == Task.TaskStatus.IN_PROGRESS:
        return render(
            request,
            'task/messages/progress_status.html',
            {'title': 'Завдання виконується'},
        )
    return render(
        request, 'task/updated_task_status_message.html', 
        {'title': 'Статус завдання'},
        )
