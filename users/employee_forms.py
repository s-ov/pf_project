from django import forms

from .models import Employee


class EmployeeRegistrationForm(forms.ModelForm):
    """
    A form for employee registration, extending Django's ModelForm.

    Fields:
        - cell_number: Employee's mobile number, used as a unique identifier.
        - first_name: Employee's first name.
        - last_name: Employee's last name.
        - admission_group: The employee's level of electrical safety clearance, chosen from predefined options.
        - password: The employee's password for account authentication.
        - confirm_password: A confirmation field to ensure the password is entered correctly.

    Widgets:
        - password: Uses PasswordInput widget to obscure the password input.
        - confirm_password: Uses PasswordInput widget to obscure the confirm password input.

    Meta:
        - model: The form is linked to the `Employee` model.
        - fields: Specifies the fields included in the form, including custom `password` and `confirm_password` fields.
    """
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Підтвердити пароль', widget=forms.PasswordInput)


    class Meta:
        model = Employee
        fields = [
            'cell_number', 
            'first_name', 
            'last_name', 
            'admission_group',
            'email', 
            'password',
            ]

    def __init__(self, *args, **kwargs):
        super(EmployeeRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            self.fields['cell_number'].label = 'Номер мобільного'
            self.fields['cell_number'].widget.attrs['placeholder'] = '+380501234567'
            self.fields['first_name'].label = 'Ім\'я'
            self.fields['last_name'].label = 'Прізвище'
            self.fields['admission_group'].label = 'Група допуску'

            self.fields['cell_number'].error_messages.update({
            'required': 'Номер мобільного обов’язково.',
            'invalid': 'Введіть правильний номер мобільного.',
            'unique': 'Цей номер вже зареєстровано.',
            })
            self.fields['password'].error_messages.update({
                'required': 'Пароль обов’язковий.',
            })

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Паролі не співпадають.')
        return cleaned_data
        

class EmployeeAdmissionGroupUpdateForm(forms.ModelForm):
    """Form for status updating"""

    class Meta:
        model = Employee
        fields = ['admission_group',]
        widgets = {
            'admission_group': forms.Select(attrs={'class': 'form-control'}),
            }
        labels = {
            'admission_group': 'Виберіть групу допуску',  
        }
