from django.core.mail import send_mail

from schedules.models import Schedule
from tdd_mail_app.settings import EMAIL_HOST_USER
from utils.models import COMPLETED, ACTIVE, NOT_ADDED, PAUSED


def task_remove_completed_schedules():
    pass


def task_start_notadded_schedules():
    pass


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


def discover_completed_schedules():
    return Schedule.objects.filter(status=COMPLETED)


def discover_active_schedules():
    return Schedule.objects.filter(status=ACTIVE)


def discover_notadded_schedules():
    return Schedule.objects.filter(status=NOT_ADDED)
