# Generated by Django 5.1.4 on 2024-12-24 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Simulator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('interval', models.CharField(choices=[('@hourly', 'Hourly'), ('@daily', 'Daily'), ('@weekly', 'Weekly'), ('@monthly', 'Monthly')], max_length=10)),
                ('kpi_id', models.IntegerField()),
            ],
        ),
    ]