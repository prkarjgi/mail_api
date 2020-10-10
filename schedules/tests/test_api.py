from datetime import timedelta, date

from django.test import TestCase

from schedules.serializers import ScheduleSerializer, RecipientSerializer
from schedules.models import Schedule, Recipient


class ScheduleSerializerTest(TestCase):
    def test_schedule_serializer_data(self):
        r1 = Recipient.objects.create(
            email_address="test1@test.com",
            name="test1"
        )
        r2 = Recipient.objects.create(
            email_address="test2@test.com",
            name="test1"
        )

        start_date = date.today()
        end_date = start_date + timedelta(days=1)
        s1 = Schedule.objects.create(
            start_date=start_date,
            end_date=end_date
        )

        s1.recipients.add(r1, r2)

        sched_serial = ScheduleSerializer(instance=s1)
        print(sched_serial.data)
