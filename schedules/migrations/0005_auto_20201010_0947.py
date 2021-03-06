# Generated by Django 3.1.2 on 2020-10-10 09:47

from django.db import migrations, models
import django.utils.timezone
import schedules.models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0004_auto_20201010_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
