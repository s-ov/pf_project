from django.urls import path 

from .views import (
    create_task_assignment_view, 
    get_task_doers_view,
    get_doer_tasks_view,
    )

app_name = "workflow"

urlpatterns = [m
    path(
        'create_task_assignment/', 
        create_task_assignment_view, 
        name="create_task_assignment",
        ), 
    path(
        'task_doers_list/', 
        get_task_doers_view, 
        name="task_doers_list",
        ), 
    path(
        'doer_tasks/<int:doer_id>/', 
        get_doer_tasks_view, 
        name="doer_tasks",
        ),
    ]
