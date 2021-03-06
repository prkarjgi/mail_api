from django.core.mail import send_mail

from schedules.models import Schedule, Interval
from mail_api.settings import EMAIL_HOST_USER


def discover_schedules(status_choice):
    return Schedule.objects.filter(status=status_choice)
