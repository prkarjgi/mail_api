from datetime import timedelta, date

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models


END_DATE_LESS_THAN_START_DATE_ERROR = "end_date cannot be less than start_date"
START_DATE_NOT_ADDED_ERROR = "start_date cannot be empty"
END_DATE_NOT_ADDED_ERROR = "end_date cannot be empty"
START_DATE_CANNOT_BE_BEFORE_TODAY_ERROR = "start_date cannot be in the past"


def delay():
    return timezone.now() + timedelta(seconds=10)


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
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)

    def save(self, *args, **kwargs):
        # there must be valid start_date and end_date values
        # check for valid start_date values
        if self.start_date:
            if self.start_date < date.today():
                raise ValidationError(START_DATE_CANNOT_BE_BEFORE_TODAY_ERROR)
        else:
            raise ValidationError(START_DATE_NOT_ADDED_ERROR)

        # check for valid end_date values
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError(END_DATE_LESS_THAN_START_DATE_ERROR)
        else:
            raise ValidationError(END_DATE_NOT_ADDED_ERROR)

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('content', 'frequency', 'start_date', 'end_date')
        ordering = ('id',)
