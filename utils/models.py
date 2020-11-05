from datetime import date, timedelta


ACTIVE = "AC"
NOT_ADDED = "NA"
COMPLETED = "CO"
PAUSED = "PA"

SCHEDULE_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (NOT_ADDED, "Not Added to Celery Beat"),
    (COMPLETED, "Completed"),
    (PAUSED, "Paused")
]


def default_end_date():
    return date.today() + timedelta(days=1)
