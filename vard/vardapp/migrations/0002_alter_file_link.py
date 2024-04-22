# Generated by Django 4.2.11 on 2024-04-21 18:34

import django.core.validators
from django.db import migrations, models
import vardapp.utils


class Migration(migrations.Migration):

    dependencies = [
        ('vardapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='link',
            field=models.FileField(blank=True, upload_to=vardapp.utils.user_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'csv', 'json'])], verbose_name='link of file'),
        ),
    ]
