# Generated by Django 2.0.6 on 2022-04-19 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0019_auto_20220419_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature_selection',
            name='vipComponent',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
