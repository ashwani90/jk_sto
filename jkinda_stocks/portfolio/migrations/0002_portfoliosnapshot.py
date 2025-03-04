# Generated by Django 5.0.1 on 2024-01-22 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortfolioSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snapshot', models.JSONField()),
                ('date', models.DateField()),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='portfolio.portfolio')),
            ],
        ),
    ]
