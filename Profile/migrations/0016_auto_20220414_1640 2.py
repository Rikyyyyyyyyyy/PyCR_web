# Generated by Django 2.0.6 on 2022-04-14 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0015_alter_feature_selection_graph1'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Project_1',
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='isExternal',
            field=models.CharField(choices=[('True', 'TRUE'), ('False', 'FALSE')], default='True', max_length=40),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='isMotabo',
            field=models.CharField(choices=[('True', 'TRUE'), ('False', 'FALSE')], default='False', max_length=40),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='isQC',
            field=models.CharField(choices=[('True', 'TRUE'), ('False', 'FALSE')], default='False', max_length=40),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='iterations',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='motaboFile',
            field=models.FileField(blank=True, default=0, null=True, upload_to='featureSelection/motabo'),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='rankingAlgorithm',
            field=models.CharField(choices=[('fisher', 'FISHER'), ('vip score', 'VIP SCORE'), ('Selectivity', 'SELECTIVITY')], default='fisher', max_length=40),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='rocType',
            field=models.CharField(choices=[('roc', 'ROC'), ('micro', 'MICRO')], default='roc', max_length=40),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='sampleName_file',
            field=models.FileField(blank=True, default=0, null=True, upload_to='featureSelection/sampleName'),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='scaleType',
            field=models.CharField(choices=[('autoscale', 'autoSCALE'), ('svnscale', 'SVN')], default='autoscale', max_length=40),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='splitRatio',
            field=models.FloatField(blank=True, default=0.5, null=True),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='survivalRate',
            field=models.FloatField(blank=True, default=0.85, null=True),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='tupaType',
            field=models.CharField(choices=[('tupa', 'TUPA'), ('classtupa', 'classTUPA'), ('notupa', 'noTUPA')], default='classtupa', max_length=40),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='variableName_file',
            field=models.FileField(blank=True, default=0, null=True, upload_to='featureSelection/variableName'),
        ),
        migrations.AddField(
            model_name='feature_selection',
            name='vipComponent',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='feature_selection',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='feature_selection',
            name='project_output',
            field=models.FileField(blank=True, null=True, upload_to='featureSelection/out'),
        ),
        migrations.AlterField(
            model_name='feature_selection',
            name='sample_file',
            field=models.FileField(blank=True, default=0, null=True, upload_to='featureSelection/sample'),
        ),
    ]