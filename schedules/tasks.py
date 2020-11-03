from django.core.mail import send_mail

from schedules.models import Schedule


def send_email_to_schedule(schedule: Schedule):
    recipients = schedule.recipients
