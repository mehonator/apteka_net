# Generated by Django 3.2.4 on 2021-07-09 20:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_time_sheet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='first_day',
            field=models.DateField(default=datetime.date(2021, 7, 9), verbose_name='Первый день'),
        ),
    ]