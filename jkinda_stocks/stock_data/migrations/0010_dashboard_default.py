# Generated by Django 5.0.2 on 2024-03-08 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_data', '0009_dashboard_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
