# Generated by Django 5.0.2 on 2024-02-18 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock_data', '0005_chart_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialDocs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default=None)),
                ('symbol', models.CharField(default=None)),
                ('data', models.JSONField()),
                ('date', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('1', 'Annual'), ('2', 'Quarter')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Financial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('date', models.DateField()),
                ('status', models.BooleanField()),
                ('type', models.CharField(choices=[('1', 'Annual'), ('2', 'Quarter')], max_length=3)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stock_data.company')),
            ],
        ),
    ]