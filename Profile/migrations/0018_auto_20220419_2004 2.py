# Generated by Django 2.0.6 on 2022-04-19 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0017_remove_feature_selection_isqc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feature_selection',
            name='isExternal',
            field=models.CharField(default='true', max_length=40),
        ),
        migrations.AlterField(
            model_name='feature_selection',
            name='isMotabo',
            field=models.CharField(default='true', max_length=40),
        ),
        migrations.AlterField(
            model_name='feature_selection',
            name='rankingAlgorithm',
            field=models.CharField(default='fisher', max_length=40),
        ),
        migrations.AlterField(
            model_name='feature_selection',
            name='rocType',
            field=models.CharField(default='false', max_length=40),
        ),
        migrations.AlterField(
            model_name='feature_selection',
            name='scaleType',
            field=models.CharField(default='autoscale', max_length=40),
        ),
        migrations.AlterField(
            model_name='feature_selection',
            name='tupaType',
            field=models.CharField(default='classtupa', max_length=40),
        ),
    ]