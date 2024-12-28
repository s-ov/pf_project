import logging
from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404,
    )
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    login, 
    authenticate, 
    update_session_auth_hash, 
    logout,
    get_user_model,
    get_backends,
    )
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlencode


from .forms import (
    UserLoginForm,
    UserCellUpdateForm,
    UserCredentialsForm,
    UserPasswordResetForm,
    UserPasswordCheckForm,
    VerificationCodeForm,
    )
from .utils import generate_verification_code

logger = logging.getLogger(__name__)

verification_codes = {}

    
def user_login_view(request):
    """ Handle user login.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the login form on GET request.
                      Redirects to user profile on successful POST request.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cell_number = form.cleaned_data['cell_number']
            password = form.cleaned_data['password']
            employee = authenticate(request, cell_number=cell_number, password=password)
            if employee is not None:
                login(request, employee)
                url = reverse('users:employee_profile', kwargs={'employee_id': employee.pk})
                return redirect(url)  
            else:
                messages.error(request, 'Неправильний номер мобільного чи пароль.')
    else:
        form = UserLoginForm()
    context = {
        'form': form,
        'title': 'Авторизація',
        'next': request.GET.get('next', '/'),
    }
    return render(request, 'users/registration/login.html', context)



def user_logout_view(request):
    """ Handle user logout.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Redirects to home page on successful logout.
    """
    logout(request)
    return redirect(reverse('main_page')) 


def user_mobile_update_view(request):
    """ Handle user cell number update.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the user profile update form on GET request.
                      Redirects to user profile on successful POST request.
    """
    employee = request.user
    
    if request.method == 'POST':
        form = UserCellUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('users:employee_profile', employee_id=employee.id)
        else:
            messages.error(request, 'Ваші дані не вдалося оновити. Будь ласка, перевірте пароль.')
    else:
        form = UserCellUpdateForm(instance=employee)
    
    return render(request, 'users/update_mobile.html', {'form': form, 'title': 'Оновити мобільний'})


def reset_password_view(request):
    """ Handle user password change.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the password change form on GET request.
                      Redirects to user profile on successful POST request.
    """
    if request.method == 'POST':
        form = UserPasswordResetForm(request.user, request.POST)
        if form.is_valid():
            employee = form.save()
            update_session_auth_hash(request, employee)
            
            if employee.pk:  
                return redirect(reverse('users:password_change_done'))
            else:
                messages.error(request, 'Ваш пароль не вдалося оновити.')
    else:
        form = UserPasswordResetForm(request.user)
    return render(request, 'users/registration/password_change.html', {
        'form': form
    }) 


def delete_user_view(request):
    """ Handle user account deletion.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: Renders the delete user form on GET request.
                      Redirects to home page on successful POST request.
    """
    if request.method == 'POST':
        form = UserPasswordCheckForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            user.delete()
            logout(request)
            messages.success(request, 'Ваш обліковий запис було видалено.')
            return redirect(reverse('users:login'))
    else:
        form = UserPasswordCheckForm(request.user)
    
    return render(request, 'users/delete_user.html', {'form': form, 'title': 'Видалити профіль'})


def check_user_view(request):
    """View to check if a user exists and send a verification code to their email."""
    
    if request.method == 'POST':
        form = UserCredentialsForm(request.POST)
        if form.is_valid():
            cell_number = form.cleaned_data['cell_number']
            email = form.cleaned_data['email']
            
            verification_code = generate_verification_code()

            request.session['verification_code'] = verification_code
            request.session['user_email'] = email
            request.session['user_id'] = get_user_model().objects.get(email=email).id  
            send_mail(
                subject="Ваш код підтвердження",
                message=f"Ваш код підтвердження: {verification_code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return redirect(reverse('users:verify_code'))
        else:
            return render(request, 'users/check_user.html', {'form': form})
    context = {'form': UserCredentialsForm(), 'title': 'Перевірка користувача',}

    return render(request, 'users/check_user.html', context,)


def verify_code_view(request):
    """View to verify the user's code and redirect to their profile."""
    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')
        stored_code = request.session.get('verification_code')
        user_id = request.session.get('user_id')

        if entered_code == str(stored_code):
            user = get_object_or_404(get_user_model(), id=user_id)
            backend = get_backends()[0]  
            user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
            login(request, user)

            del request.session['verification_code']
            del request.session['user_id']

            return redirect('users:employee_profile', employee_id=user_id)
        else:
            return render(
                request,
                'users/verify_code.html',
                {
                    'title': 'Код підтвердження',
                    'error': 'Невірний код підтвердження. Спробуйте ще раз',
                }
            )
    return render(request, 'users/verify_code.html', {'title': 'Код підтвердження'})
