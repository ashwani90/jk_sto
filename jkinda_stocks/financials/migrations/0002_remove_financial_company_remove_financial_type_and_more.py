# Generated by Django 5.0.2 on 2024-02-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financials', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financial',
            name='company',
        ),
        migrations.RemoveField(
            model_name='financial',
            name='type',
        ),
        migrations.AddField(
            model_name='financial',
            name='symbol',
            field=models.CharField(default=None),
        ),
    ]
