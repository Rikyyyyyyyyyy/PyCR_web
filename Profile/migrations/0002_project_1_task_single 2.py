# Generated by Django 3.2.1 on 2021-08-21 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project_1',
            name='task_single',
            field=models.BooleanField(default=False),
        ),
    ]