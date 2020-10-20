from datetime import date

from django.core.exceptions import ValidationError

# Errors for Schedule Model fields
END_DATE_LESS_THAN_START_DATE_ERROR = "end_date cannot be less than start_date"
START_DATE_NOT_ADDED_ERROR = "start_date cannot be empty"
END_DATE_NOT_ADDED_ERROR = "end_date cannot be empty"
START_DATE_CANNOT_BE_BEFORE_TODAY_ERROR = "start_date cannot be in the past"

# Errors for Recipient fields
RECIPIENTS_GREATER_THAN_500_ERROR = "Recipients should be less than 500"
RECIPIENTS_CONTAIN_DUPLICATES_ERROR = "Recipients shouldn't contain duplicates"


def start_date_after_today(start_date):
    """
    there must be valid start_date and end_date values
    check for valid start_date values
    """
    if start_date:
        if start_date < date.today():
            raise ValidationError(START_DATE_CANNOT_BE_BEFORE_TODAY_ERROR)
    else:
        raise ValidationError(START_DATE_NOT_ADDED_ERROR)


def start_date_before_end_date(start_date, end_date):
    """
    check for valid end_date values
    """
    if end_date:
        if end_date < start_date:
            raise ValidationError(END_DATE_LESS_THAN_START_DATE_ERROR)
    else:
        raise ValidationError(END_DATE_NOT_ADDED_ERROR)


def recipients_less_than_500(recipients):
    if len(recipients) > 500:
        raise ValidationError(RECIPIENTS_GREATER_THAN_500_ERROR)


def recipients_not_contains_duplicates(recipients):
    recipients_set = set()
    for recipient in recipients:
        if recipient not in recipients_set:
            recipients_set.add(recipient)
        else:
            raise ValidationError(RECIPIENTS_CONTAIN_DUPLICATES_ERROR)
