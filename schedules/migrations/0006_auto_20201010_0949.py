# Generated by Django 3.1.2 on 2020-10-10 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0005_auto_20201010_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
