from datetime import datetime, date, timedelta

from schedules.serializers import ScheduleSerializer
from schedules.models import Schedule
from utils.models import default_date_time


def create_schedule_input_data(
    description="placeholder", subject="placeholder",
    content="placeholder", frequency=timedelta(days=1),
    start_date=default_date_time(),
    end_date=default_date_time(days=1), status=Schedule.NOT_ADDED,
    recipients=[]
):
    data = {}
    data['description'] = description
    data['subject'] = subject
    data['content'] = content
    data['frequency'] = frequency
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['status'] = status
    data['recipients'] = recipients
    return data


def serialize_input_data(
    description="placeholder", subject="placeholder",
    content="placeholder",
    frequency=timedelta(days=1),
    start_date=default_date_time(),
    end_date=default_date_time(days=1), status=Schedule.NOT_ADDED,
    recipients=[], num_schedules=1
):
    for num in range(num_schedules):
        data = create_schedule_input_data(
            description=description,
            subject=subject,
            content=f"{content}: {num}",
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
            status=status,
            recipients=recipients
        )
        serializer = ScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
