# Generated by Django 5.0.2 on 2024-02-19 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('data', models.JSONField()),
                ('processed', models.BooleanField(default=False)),
            ],
        ),
    ]
