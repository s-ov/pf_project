from django import forms
from django.utils.timezone import now, timedelta

from task.validators import validate_minimum_one_hour_later
from task.models import Task
from work_tower.models.node import Node
from .models import TaskAssignment
from users.models import Employee


class TaskAssignmentForm(forms.ModelForm):
    """Form to assign a task to a specific doer."""
    doer = forms.ModelChoiceField(
        queryset=Employee.objects.filter(role='Electrician'), 
        label="Виконавець:"
        )
    task_description = forms.CharField(
        widget=forms.Textarea, 
        label="Завдання:"
        )
    node = forms.ModelChoiceField(
        queryset=Node.objects.all(),
        required=False, label="Індекс вузла:"
        )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False, label="Виконати до:",
        validators=[validate_minimum_one_hour_later]
        )

    class Meta:
        model = TaskAssignment
        fields = ['doer', 'task_description', 'node', 'deadline']

    def save(self, commit=True):
        """Create a Task instance"""

        doer = self.cleaned_data['doer']
        task_description = self.cleaned_data['task_description']
        deadline = self.cleaned_data.get('deadline') or now() + timedelta(days=1)

        task = Task.objects.create(
            doer=doer,
            task_description=task_description,
            deadline=deadline
        )
        task_assignment = TaskAssignment(
            task=task,
            node=self.cleaned_data.get('node')
        )
        if commit:
            task_assignment.save()
        
        return task_assignment
