# Generated by Django 2.0.6 on 2022-04-19 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0016_auto_20220414_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature_selection',
            name='isQC',
        ),
    ]