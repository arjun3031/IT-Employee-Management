# Generated by Django 5.1.2 on 2024-10-18 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_project_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.workers'),
        ),
    ]