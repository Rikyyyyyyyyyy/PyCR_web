# Generated by Django 3.2.1 on 2021-08-21 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_project_1_task_single'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_1',
            name='task_multiple',
            field=models.BooleanField(default=False),
        ),
    ]