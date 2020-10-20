from datetime import timedelta, date

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils import timezone
from django.db import models

from utils import validators


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
    recipients = models.ManyToManyField(Recipient)
    content = models.TextField(default='', blank=True)
    frequency = models.DurationField(default=timedelta())
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)

    is_cleaned = False

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        validators.start_date_after_today(self.start_date)
        validators.start_date_before_end_date(self.start_date, self.end_date)
        self.is_cleaned = True

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('content', 'frequency', 'start_date', 'end_date')
        ordering = ('id',)
