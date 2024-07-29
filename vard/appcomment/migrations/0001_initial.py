# Generated by Django 4.2.11 on 2024-07-29 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_send', models.DateTimeField(auto_now_add=True, verbose_name='date of send')),
                ('date_remove', models.DateTimeField(auto_now_add=True, verbose_name='date of remove')),
                ('date_delivery', models.DateTimeField(auto_now_add=True, verbose_name='date of delivery')),
                ('comment', models.TextField(verbose_name='comment')),
            ],
        ),
        migrations.CreateModel(
            name='ReadComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_reading', models.DateTimeField(auto_now_add=True, verbose_name='date of read')),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appcomment.comment', verbose_name='id of comment')),
            ],
        ),
    ]
