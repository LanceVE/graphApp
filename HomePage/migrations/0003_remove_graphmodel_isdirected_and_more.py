# Generated by Django 5.0.6 on 2024-06-27 22:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0002_graphmodel_delete_graphstartnode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graphmodel',
            name='isdirected',
        ),
        migrations.RemoveField(
            model_name='graphmodel',
            name='startingnode',
        ),
        migrations.AlterField(
            model_name='graphmodel',
            name='txt',
            field=models.FileField(upload_to='graph/txt/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])]),
        ),
    ]
