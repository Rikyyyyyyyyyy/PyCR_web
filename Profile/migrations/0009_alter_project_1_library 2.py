# Generated by Django 3.2.1 on 2021-08-24 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0008_auto_20210824_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project_1',
            name='Library',
            field=models.FileField(blank=True, default=0, null=True, upload_to='project1/Lib'),
        ),
    ]
