# Generated by Django 4.2.11 on 2024-07-29 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
                ('date_change', models.DateTimeField(auto_now=True, verbose_name='date of change')),
                ('str_query', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChartDashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ClientData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClientDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_name', models.CharField(default='', max_length=255)),
                ('user_name', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=128)),
                ('driver', models.IntegerField(choices=[(1, 'SQLAlchemy for MySQL')], default=1)),
                ('url', models.CharField(max_length=255, null=True)),
                ('host', models.CharField(default='localhost', max_length=60, null=True)),
                ('port', models.IntegerField(default=3306, null=True)),
                ('data_base_type', models.CharField(max_length=255, null=True)),
                ('data_base_name', models.CharField(max_length=63)),
                ('description', models.CharField(max_length=255, null=True)),
                ('str_datas_for_connection', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date of creation')),
                ('date_change', models.DateTimeField(auto_now=True, verbose_name='date of change')),
                ('chart', models.ManyToManyField(blank=True, through='appchart_DB.ChartDashboard', to='appchart_DB.chart')),
            ],
        ),
    ]
