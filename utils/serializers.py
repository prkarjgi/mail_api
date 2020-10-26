from typing import List, Dict

from schedules.models import Schedule, Recipient


def get_or_create_recipient(recipient: Dict):
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
        new_recipient, new_created = get_or_create_recipient(recipient)
        if new_created:
            to_be_created.append(new_recipient)
        new_recipients.append(new_recipient)

    Recipient.objects.bulk_create(to_be_created)
    schedule.recipients.add(*new_recipients)


def update_recipients_in_schedule(schedule: Schedule, recipients: List):
    """
    Get existing email addresses associated with the provided schedule.
    Check which addresses should be deleted from the relationship table
    and bulk delete them


    """
    pass
