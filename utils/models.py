from datetime import date, timedelta


ACTIVE = "AC"
NOT_SCHEDULED = "NS"
COMPLETED = "CO"

schedule_status_choices = [
    (ACTIVE, "Active"),
    (NOT_SCHEDULED, "Not Scheduled"),
    (COMPLETED, "Completed")
]


def default_end_date():
    return date.today() + timedelta(days=1)
