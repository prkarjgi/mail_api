from datetime import timedelta, date

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils import timezone
from django.db import models

from utils import validators, models as utils_models


class Recipient(models.Model):
    email_address = models.EmailField(
        default="dummy@placeholder.com",
        unique=True,
        validators=[EmailValidator]
    )
    name = models.TextField(default='')

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f"{self.name}: {self.email_address}"


class Schedule(models.Model):
    ACTIVE = "AC"
    NOT_ADDED = "NA"
    COMPLETED = "CO"
    PAUSED = "PA"

    SCHEDULE_STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (NOT_ADDED, "Not Added to Celery Beat"),
        (COMPLETED, "Completed"),
        (PAUSED, "Paused")
    ]

    description = models.TextField(default='', blank=True)
    subject = models.TextField(default='', blank=True)
    recipients = models.ManyToManyField(Recipient)
    content = models.TextField(default='', blank=True)
    frequency = models.DurationField(default=timedelta(0))
    start_date = models.DateTimeField(default=utils_models.default_start_date)
    end_date = models.DateTimeField(default=utils_models.default_end_date)
    status = models.CharField(
        max_length=2,
        choices=SCHEDULE_STATUS_CHOICES,
        default=NOT_ADDED
    )

    is_cleaned = False

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        validators.start_date_after_today(self.start_date)
        validators.start_date_before_end_date(self.start_date, self.end_date)
        validators.frequency_not_greater_than_end_date(
            self.frequency, self.start_date, self.end_date
        )
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (
            'description', 'subject', 'content', 'frequency',
            'start_date', 'end_date'
        )
        ordering = ('id',)


class Interval(models.Model):
    interval = models.DurationField(
        default=timedelta(0), unique=True, null=False
    )
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id',)
