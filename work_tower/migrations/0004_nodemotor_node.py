# Generated by Django 4.2.17 on 2024-12-15 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_tower', '0003_motorcontrolcenter'),
    ]

    operations = [
        migrations.CreateModel(
            name='NodeMotor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('power', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('round_per_minute', models.PositiveSmallIntegerField(default=0)),
                ('connection', models.CharField(choices=[('▲', 'Трикутник'), ('✳', 'Зірка')], default='▲', max_length=1)),
                ('amperage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
            ],
            options={
                'verbose_name': 'Двигун вузла',
                'verbose_name_plural': 'Двигуни',
                'unique_together': {('power', 'round_per_minute', 'connection', 'amperage')},
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Засувка', 'Засувка'), ('Засувка загружна', 'Засувка загружна'), ('Засувка вигружна', 'Засувка вигружна'), ('Kонвеєр', 'Kонвеєр'), ('Норія', 'Норія'), ('Пробовідбірник', 'Пробовідбірник'), ('Вент. аспіраційний', 'Вент. аспіраційний'), ('Вент. аераційний', 'Вент. аераційний'), ('Сепаратор очистки', 'Сепаратор очистки'), ('Клапан перекидний', 'Клапан перекидний'), ('Клапан 3-х ходовий', 'Клапан 3-х ходовий'), ('Вентилятор', 'Вентилятор'), ('Вентилятор даховий', 'Вентилятор даховий'), ('Шнек зачисний', 'Шнек зачисний')], max_length=25)),
                ('index', models.CharField(max_length=30, unique=True)),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nodes', to='work_tower.worktowerlevel')),
                ('mcc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mcc', to='work_tower.motorcontrolcenter')),
                ('motor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='nodes', to='work_tower.nodemotor')),
            ],
            options={
                'verbose_name': 'Вузол',
                'verbose_name_plural': 'Вузли',
            },
        ),
    ]