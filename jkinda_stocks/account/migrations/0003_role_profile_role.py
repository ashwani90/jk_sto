# Generated by Django 5.0.2 on 2024-03-02 12:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_organization_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='account.role'),
        ),
    ]
