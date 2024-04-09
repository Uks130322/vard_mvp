# Generated by Django 4.2.11 on 2024-04-03 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appquery', '0005_remove_clientdb_result_query_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, null=True)),
                ('chart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appquery.chart')),
            ],
        ),
    ]
