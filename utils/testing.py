from datetime import date, timedelta


def create_schedule_input_data(
    description="placeholder",
    content="placeholder", frequency=timedelta(days=1),
    start_date=date.today(),
    end_date=date.today() + timedelta(days=1), recipients=[]
):
    data = {}
    data['description'] = description
    data['content'] = content
    data['frequency'] = frequency
    data['start_date'] = start_date
    data['end_date'] = end_date
    data['recipients'] = recipients
    return data
