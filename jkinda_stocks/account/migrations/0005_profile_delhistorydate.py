# Generated by Django 5.0.3 on 2024-03-28 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_profile_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='delHistoryDate',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
