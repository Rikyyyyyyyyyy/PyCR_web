# Generated by Django 3.0.6 on 2022-10-28 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0008_auto_20221028_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature_selection',
            name='is_exMotabo',
            field=models.CharField(blank=True, default='true', max_length=40),
        ),
    ]
