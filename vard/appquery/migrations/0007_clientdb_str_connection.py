# Generated by Django 4.2.11 on 2024-04-03 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appquery', '0006_clientdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientdb',
            name='str_connection',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
