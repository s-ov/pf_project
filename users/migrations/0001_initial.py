# Generated by Django 4.2.17 on 2024-12-17 21:42

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('cell_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="Номер має бути '+38', потім код оператора, а потім ще 7 цифр номеру. Наприклад: +380501234567", regex='^\\+38(050|066|095|099|067|068|096|097|098|063|073|093|091)\\d{7}$')], verbose_name='Мобільний')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, validators=[django.core.validators.EmailValidator()])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_set', related_query_name='customuser', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', related_query_name='customuser', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('role', models.CharField(choices=[('Engineer', 'Інженер'), ('Electrician', 'Електрик')], default='Electrician', max_length=15)),
                ('admission_group', models.CharField(blank=True, choices=[('І-ша група з електробезпеки', 'I'), ('ІI-а група з електробезпеки', 'II'), ('ІII-тя група з електробезпеки', 'III'), ('ІV-а до 1000V група з електробезпеки', 'IV до 1kV'), ('ІV-а вище 1000V група з електробезпеки', 'IV вище 1kV'), ('V-а група з електробезпеки', 'V'), ('Не вибрано', 'Не вибрано')], default='Не вибрано', max_length=130, null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('users.customuser',),
        ),
    ]
