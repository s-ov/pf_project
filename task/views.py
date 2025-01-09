from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import Http404
from django.utils.timezone import now, timedelta

from .models import Task, TaskArchive
from .forms import StatusUpdateForm
from .utils import task_update_message

Doer = get_user_model()


class DoerTasksListView(ListView):
    """Retrieve and display all tasks for a specific doer."""
    model = Task
    template_name = 'task/doer_tasks.html'  
    context_object_name = 'tasks'
    paginate_by = 2

    def get_queryset(self):
        doer_id = self.kwargs.get('doer_id')
        doer = get_object_or_404(get_user_model(), id=doer_id)
        
        return Task.objects.filter(doer=doer)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doer'] = get_object_or_404(
                                            get_user_model(), 
                                            id=self.kwargs.get('doer_id'),
                                            )
        context['title'] = 'Завдання'
        return context



class TaskStatusUpdateView(UpdateView):
    """The view updates Task status"""
    model = Task
    form_class = StatusUpdateForm
    template_name = 'task/task_status_form.html'
    context_object_name = 'task'

    def post(self, request, pk):
        try:
            task = get_object_or_404(Task, id=pk)
        except Http404:
            return render(request, 'task/error_no_task.html', {'title': 'Нема завдання'})

        new_status = request.POST.get('status')
        deadline = request.POST.get('deadline')

        if new_status == Task.TaskStatus.CANCELED:
            task.delete()
            return task_update_message(request, Task.TaskStatus.CANCELED) 
        
        if new_status in [
            Task.TaskStatus.COMPLETED, 
            Task.TaskStatus.PENDING, 
            Task.TaskStatus.IN_PROGRESS,
            ]:
            task.status = new_status

            if new_status == Task.TaskStatus.PENDING:
                task.deadline = None  
            elif new_status == Task.TaskStatus.IN_PROGRESS:
                task.deadline = deadline if deadline else now() + timedelta(days=1)

            task.save()
            return task_update_message(request, new_status)

        task.status = new_status
        task.save()

        return task_update_message(request, new_status)

    def get_employee(self, user):
        """Check if the user model has 'get_employee' method and retrieve employee."""
        if hasattr(user, 'get_employee') and callable(getattr(user, 'get_employee')):
            return user.get_employee()
        else:
            messages.error(self.request, "Employee data could not be retrieved.")
            return None

    def get_form(self, form_class=None):
        """Customize form to restrict 'CANCELED' choice for Electricians."""
        form = super().get_form(form_class)
        employee = self.get_employee(self.request.user)

        if employee and employee.role == employee.Role.ELECTRICIAN:
            form.fields['status'].choices = [
                choice for choice in Task.TaskStatus.choices if choice[0] != Task.TaskStatus.CANCELED
            ]
        return form

    def form_valid(self, form):
        """Handle form submission with role-based validation."""
        task = form.instance
        new_status = form.cleaned_data['status']
        employee = self.get_employee(self.request.user)
        form.save()
        return redirect(reverse_lazy('task:doer_tasks', kwargs={'doer_id': task.doer.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оновити статус'
        return context


def get_archived_tasks_view(request):
    """Get all archived tasks"""
    archived_tasks = TaskArchive.objects.all()
    context = {'archived_tasks': archived_tasks, 'title': 'Архів',}
    return render(request, 'task/archived_tasks.html', context)
    
    
