# Generated by Django 5.1.2 on 2024-10-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workers',
            name='certificate',
            field=models.FileField(null=True, upload_to='certificates/'),
        ),
        migrations.AlterField(
            model_name='workers',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]