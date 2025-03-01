# Generated by Django 5.1.2 on 2024-10-26 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_alter_dailyreport_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dailyreport',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='work_report',
            field=models.FileField(blank=True, null=True, upload_to='daily_reports_teamleaders/'),
        ),
        migrations.RemoveField(
            model_name='dailyreport',
            name='developer',
        ),
    ]
