from django import forms

from .validators import validate_minimum_one_hour_later
from .models import Task


class StatusUpdateForm(forms.ModelForm):
    """Form for status updating"""
    
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False, label="Виконати до:",
        validators=[validate_minimum_one_hour_later]
        )

    class Meta:
        model = Task
        fields = ['status', 'deadline',]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            }
        labels = {
            'status': 'Виберіть статус:',  
        }
        

