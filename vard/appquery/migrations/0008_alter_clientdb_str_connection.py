# Generated by Django 4.2.11 on 2024-04-03 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appquery', '0007_clientdb_str_connection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdb',
            name='str_connection',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
