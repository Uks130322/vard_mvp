# Generated by Django 4.2.11 on 2024-07-25 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
                ('theme', models.CharField(max_length=255, verbose_name='theme of feedback')),
                ('description', models.TextField(verbose_name='feedback')),
            ],
        ),
    ]
