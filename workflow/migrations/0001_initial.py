# Generated by Django 4.2.17 on 2024-12-28 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task', '0002_taskarchive'),
        ('work_tower', '0004_nodemotor_node'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='work_tower.node')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='task.task')),
            ],
        ),
    ]