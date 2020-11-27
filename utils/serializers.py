from typing import List, Dict
from datetime import timedelta

from schedules.models import Schedule, Recipient, Interval
from schedules import tasks
from mail_api.celery import app


def create_or_get_recipient(recipient: Dict):
    email_address = recipient.get('email_address')
    new_created = False
    if Recipient.objects.filter(email_address=email_address).exists():
        new_recipient = Recipient.objects.get(email_address=email_address)
    else:
        new_recipient = Recipient(**recipient)
        new_created = True
    return new_recipient, new_created


def create_or_update_recipients(
    schedule: Schedule, recipients: List, update: bool
):
    new_recipients, to_be_created = [], []

    if update:
        schedule.recipients.clear()

    for recipient in recipients:
        new_recipient, new_created = create_or_get_recipient(recipient)
        if new_created:
            to_be_created.append(new_recipient)
        new_recipients.append(new_recipient)

    Recipient.objects.bulk_create(to_be_created)
    schedule.recipients.add(*new_recipients)


def create_or_get_interval(schedule: Schedule):
    frequency = schedule.frequency
    if not Interval.objects.filter(interval=frequency).exists():
        interval = Interval.objects.create(interval=frequency)
        app.conf.beat_schedule[str(interval.interval)] = {
            'task': 'schedules.tasks.task_send_email',
            'schedule': interval.interval,
            'args': (interval.interval,),
        }
    else:
        interval = Interval.objects.get(interval=frequency)
    return interval


def encode_interval(interval: timedelta):
    pass


def decode_interval(interval: str):
    pass
