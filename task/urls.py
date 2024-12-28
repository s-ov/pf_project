from django.urls import path
from .views import (
    DoerTasksListView,
    TaskStatusUpdateView,
    
    get_archived_tasks_view,
    )


app_name = "task"

urlpatterns = [
    path(
        'doer_tasks/<int:doer_id>/', 
        DoerTasksListView.as_view(), 
        name='doer_tasks'
        ),
    path(
        'task_update_status/<int:pk>/', 
        TaskStatusUpdateView.as_view(), 
        name='task_update_status',
        ),
    path('get_archived_tasks/', get_archived_tasks_view, name='get_archived_tasks'),

]
