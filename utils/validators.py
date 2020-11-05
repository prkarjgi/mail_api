from datetime import date, timedelta
from re import search

from rest_framework.serializers import ValidationError
from django.core import exceptions
from django.utils import timezone

from utils.models import default_date_time

# Errors for Schedule Model fields
END_DATE_LESS_THAN_START_DATE_ERROR = "end_date cannot be less than start_date"
START_DATE_NOT_ADDED_ERROR = "start_date cannot be empty"
END_DATE_NOT_ADDED_ERROR = "end_date cannot be empty"
FREQUENCY_NOT_ADDED_ERROR = "frequency cannot be empty"
START_DATE_CANNOT_BE_BEFORE_TODAY_ERROR = "start_date cannot be in the past"
FREQUENCY_GREATER_THAN_END_DATE_ERROR = "frequency cannot exceed end_date"
FIELDS_NOT_UNIQUE_TOGETHER_ERROR = "Schedule fields should be unique together"

# Errors for Recipient fields
RECIPIENTS_GREATER_THAN_500_ERROR = "Recipients should be less than 500"
RECIPIENTS_CONTAIN_DUPLICATES_ERROR = "Recipients shouldn't contain duplicates"
INVALID_EMAIL_ADDRESS_ERROR = "Enter a valid email address."


def frequency_not_greater_than_end_date(frequency, start_date, end_date):
    """
    check for start_date + frequency <= end_date.
    else it is invalid since this case would be useless
    """
    if frequency is not None:
        if start_date + frequency > end_date:
            raise exceptions.ValidationError(
                FREQUENCY_GREATER_THAN_END_DATE_ERROR
            )
    else:
        raise exceptions.ValidationError(FREQUENCY_NOT_ADDED_ERROR)


def start_date_after_today(start_date):
    """
    there must be valid start_date and end_date values
    check for valid start_date values
    """
    if start_date:
        if start_date < default_date_time():
            raise exceptions.ValidationError(
                START_DATE_CANNOT_BE_BEFORE_TODAY_ERROR
            )
    else:
        raise exceptions.ValidationError(START_DATE_NOT_ADDED_ERROR)


def start_date_before_end_date(start_date, end_date):
    """
    check for valid end_date values
    """
    if end_date:
        if end_date < start_date:
            raise exceptions.ValidationError(
                END_DATE_LESS_THAN_START_DATE_ERROR
            )
    else:
        raise exceptions.ValidationError(END_DATE_NOT_ADDED_ERROR)


def recipients_less_than_500(recipients):
    if len(recipients) > 500:
        raise ValidationError(RECIPIENTS_GREATER_THAN_500_ERROR)


def recipients_not_contains_duplicates(recipients):
    recipients_set = set()
    for recipient in recipients:
        if recipient['email_address'] not in recipients_set:
            recipients_set.add(recipient['email_address'])
        else:
            raise ValidationError(RECIPIENTS_CONTAIN_DUPLICATES_ERROR)


class RecipientDuplicateValidator:
    def __init__(self):
        requires_context = True

    def __call__(self, serializer_field):
        recipients_set = set()
        for recipient in serializer_field:
            if recipient['email_address'] not in recipients_set:
                recipients_set.add(recipient['email_address'])
            else:
                raise ValidationError(RECIPIENTS_CONTAIN_DUPLICATES_ERROR)


def is_valid_email_address(email_address):
    return search(r"[a-zA-Z0-9.]+@[a-zA-Z0-9.]+\.[a-zA-Z]+", email_address)
