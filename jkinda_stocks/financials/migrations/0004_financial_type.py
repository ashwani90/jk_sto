# Generated by Django 5.0.2 on 2024-02-23 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0003_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='financial',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]