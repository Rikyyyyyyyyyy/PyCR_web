# Generated by Django 3.2.1 on 2021-08-21 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0003_project_1_task_multiple'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_1',
            name='ms_file',
            field=models.FileField(null=True, upload_to='project1/ms'),
        ),
    ]
