# Generated by Django 4.2.11 on 2024-07-30 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='access',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owne', to=settings.AUTH_USER_MODEL, verbose_name='owner id'),
        ),
    ]
