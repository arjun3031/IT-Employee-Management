# Generated by Django 5.1.2 on 2024-10-18 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_client_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='project_name',
        ),
    ]
