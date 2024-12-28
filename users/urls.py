from django.urls import path
from django.contrib.auth.views import PasswordChangeDoneView

from .views import ( 
    user_login_view,
    user_logout_view,
    user_mobile_update_view,
    reset_password_view,
    delete_user_view,
    check_user_view,
    verify_code_view
    )

from .employee_views import ( 
    employee_register_view,
    employee_profile_view,
    get_electricians_view,
    update_employee_admission_group_view, 
    )


app_name = 'users'

urlpatterns = [
    path('register/', employee_register_view, name='register'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),

    path('employee_profile/<int:employee_id>/', employee_profile_view, name='employee_profile'),
    path('update_mobile/', user_mobile_update_view, name='update_mobile'),
    path('reset_password/', reset_password_view, name='reset_password'),
    path(
        'password_change_done/', 
         PasswordChangeDoneView.as_view(template_name='users/registration/password_change_done.html'), 
         name='password_change_done'
         ),

    path('delete_account/', delete_user_view, name='delete_account'),

    path('electricians_list', get_electricians_view, name='electricians_list'),

    path(
        'update-admission-group/<int:employee_id>/', 
        update_employee_admission_group_view, 
        name='update_admission_group'),

    path('check_user/', check_user_view, name='check_user'),
    path('verify_code/', verify_code_view, name='verify_code'),
]
