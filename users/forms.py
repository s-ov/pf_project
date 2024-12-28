from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model, authenticate

CustomUser = get_user_model()


class UserLoginForm(forms.Form):
    cell_number = forms.CharField(
        max_length=13,
        label='Номер мобільного',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380501234567'
        },
        )
    )
    password = forms.CharField(
        max_length=50,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Введіть Ваш пароль'
            })
    )


class UserCellUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 
                                                                 'placeholder': 'Введіть Ваш пароль'}
                                                        )
                               )

    class Meta:
        model = CustomUser
        fields = ['cell_number',]
        widgets = {
            'cell_number': forms.TextInput(attrs={'class': 'form-control'}),
            }
        labels = {
            'cell_number': 'Номер мобільного',  
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user = authenticate(username=self.instance.cell_number, password=password)
        if not user:
            raise forms.ValidationError('Невірний пароль.')
        return cleaned_data


class UserPasswordResetForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть старий пароль'}),
        error_messages = {
            'password_incorrect': 'Введіть правильний пароль.', 
            'required': 'Будь ласка, введіть старий пароль.'
            }
    )
    new_password1 = forms.CharField(
        max_length=50,
        min_length=8,
        label="Новий пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть новий пароль'}),
        error_messages={
            'required': 'Будь ласка, введіть новий пароль.',
            'max_length': 'Пароль занадто довгий: не більше 50 символів.',
            'min_length': 'Пароль занадто короткий: не менше 8 символів.',
        }
    )
    new_password2 = forms.CharField(
        label="Новий пароль (підтвердження)",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердіть новий пароль'}),
        error_messages={
            'required': 'Будь ласка, підтверджте новий пароль.',
            'password_mismatch': 'Новий пароль і підтвердження паролю не співпадають.',
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                self.add_error('new_password2', 'Паролі не збігаються.')
        return cleaned_data


class UserPasswordCheckForm(forms.Form):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={ 
                                        'class': 'form-control', 
                                        'placeholder': 'Введіть пароль'
                                        }
                                    ),
        strip=False,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.user.check_password(password):
            raise forms.ValidationError("Невірний пароль. Будь ласка, спробуйте ще раз.")
        return password


class UserCredentialsForm(forms.Form):
    """Form to check if a user exists and validate their email."""
    cell_number = forms.CharField(
        max_length=15,
        label="Мобільний номер:",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380501234567'
        },
        ),
    )
    email = forms.EmailField(
        label="Email:",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть Вашу електронну пошту'
        },
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        cell_number = cleaned_data.get('cell_number')
        email = cleaned_data.get('email')

        if cell_number and email:
            try:
                user = CustomUser.objects.get(cell_number=cell_number)
                if user.email != email:
                    self.add_error('email', 
                                   "Вказаний email не збігається з електронною поштою,\
                                   зареєстрованою для цього номера телефону."
                    )
            except CustomUser.DoesNotExist:
                self.add_error('email', 'Користувача з таким номером телефону не знайдено.')
        else:
            self.add_error('email', 'Будь ласка, введіть номер телефону та електронну пошту')
        return cleaned_data

class VerificationCodeForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    verification_code = forms.CharField(label="Verification Code", max_length=6, required=True)
