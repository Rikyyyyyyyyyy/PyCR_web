# Generated by Django 3.2.1 on 2021-08-24 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0007_project_1_single_ms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_1',
            name='Library',
            field=models.FileField(blank=True, default=0, upload_to='project1/Lib'),
        ),
        migrations.AlterField(
            model_name='project_1',
            name='ms_file',
            field=models.FileField(default=0, null=True, upload_to='project1/ms'),
        ),
    ]