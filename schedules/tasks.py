from datetime import timedelta

from celery import shared_task
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail

from schedules.models import Schedule, Interval
from tdd_mail_app.settings import EMAIL_HOST_USER
from utils.tasks import discover_schedules


@shared_task
def task_send_email(interval: Interval):
    now = timezone.now()
    interval = interval.interval
    end_limit = now + interval
    schedules = Schedule.objects.filter(
        Q(frequency=interval.interval),
        Q(status=Schedule.ACTIVE) | Q(status=Schedule.NOT_ADDED),
    )

    for schedule in schedules:
        if end_limit >= schedule.end_date:
            schedule.status = Schedule.COMPLETED
            schedule.save()

        if schedule.status == Schedule.NOT_ADDED:
            if schedule.start_date <= now and schedule.end_date >= end_limit:
                schedule.status = Schedule.ACTIVE
                schedule.save()

        if schedule.status == Schedule.ACTIVE:
            send_email_to_schedule(schedule=schedule)


@shared_task
def send_email_to_schedule(schedule: Schedule):
    recipient_list = [
        recipient.email_address for recipient in schedule.recipients.all()
    ]
    send_mail(
        subject=schedule.subject,
        message=schedule.content,
        from_email=EMAIL_HOST_USER,
        recipient_list=recipient_list
    )
