# Generated by Django 5.1.2 on 2024-10-24 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
