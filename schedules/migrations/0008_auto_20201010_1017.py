# Generated by Django 3.1.2 on 2020-10-10 10:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0007_auto_20201010_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]