# Generated by Django 5.0.6 on 2024-07-04 18:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0004_remove_graphmodel_txt_graphmodel_graph'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphmodel',
            name='graph',
            field=models.FileField(upload_to='graphApp/static/graphApp/text', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])]),
        ),
    ]
