# Generated by Django 5.1.2 on 2024-10-24 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_work_end_date_work_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='work',
            name='submit_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='upload',
            field=models.FileField(blank=True, null=True, upload_to='work_submissions/'),
        ),
    ]
