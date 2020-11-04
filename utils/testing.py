from datetime import date, timedelta

from schedules.serializers import ScheduleSerializer


def create_schedule_input_data(
    description="placeholder", subject="placeholder",
    content="placeholder", frequency=timedelta(days=1),
    start_date=date.today(),
    end_date=date.today() + timedelta(days=1), recipients=[]
):
    data = {}
    data['description'] = description
    data['subject'] = subject
    data['content'] = content
    data['frequency'] = frequency
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['recipients'] = recipients
    return data


def serialize_input_data(
    description="placeholder", subject="placeholder",
    content="placeholder",
    frequency=timedelta(days=1),
    start_date=date.today(),
    end_date=date.today() + timedelta(days=1), recipients=[],
    num_schedules=1,
    serializer_class=ScheduleSerializer
):
    for num in range(num_schedules):
        data = create_schedule_input_data(
            description=description,
            subject=subject,
            content=f"{content}: {num}",
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
            recipients=recipients
        )
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
