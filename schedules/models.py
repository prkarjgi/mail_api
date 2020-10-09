from datetime import timedelta

from django.db import models


class Recipient(models.Model):
    email_address = models.EmailField(
        default="dummy@placeholder.com", unique=True
    )
    name = models.TextField(default='')

    class Meta:
        ordering = ('id',)


class Schedule(models.Model):
    recipients = models.ManyToManyField(Recipient)
    content = models.TextField(default='')
    frequency = models.DurationField(default=timedelta())

    class Meta:
        unique_together = ('content', 'frequency')
        ordering = ('id',)
