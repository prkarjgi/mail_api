from datetime import date, timedelta, datetime
from django.utils import timezone


def default_date_time(
    days=0, seconds=0, microseconds=0,
    milliseconds=0, minutes=0, hours=0, weeks=0,
    subtract=False
):
    now = timezone.now()
    today = datetime(
        year=now.year, month=now.month, day=now.day, tzinfo=now.tzinfo
    )
    delta = timedelta(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks
    )
    if subtract:
        return today - delta
    else:
        return today + delta


def default_end_date():
    return default_date_time(days=1)


def default_start_date():
    return default_date_time()
