# Generated by Django 5.1.2 on 2024-10-18 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_project_project_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='project_status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]