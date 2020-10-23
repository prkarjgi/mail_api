from datetime import timedelta, date
import json
import io
from unittest import skip

from django.test import TestCase

from schedules.serializers import ScheduleSerializer, RecipientSerializer
from schedules.models import Schedule, Recipient
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


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
        # print(sched_serial.data)

    def test_schedule_serializer_deserialization(self):
        r1 = Recipient.objects.create(
            name="test",
            email_address="test@gmail.com"
        )
        r2 = Recipient.objects.create(
            name="test2",
            email_address="test2@gmail.com"
        )

        start_date = date.today()
        end_date = start_date + timedelta(days=1)
        s1 = Schedule.objects.create(
            content="placeholder",
            start_date=start_date,
            end_date=end_date
        )
        s1.recipients.add(r1, r2)
        sched_serialized = ScheduleSerializer(instance=s1)

        json_data = JSONRenderer().render(sched_serialized.data)
        print(type(json_data))

        stream = io.BytesIO(json_data)
        data = JSONParser().parse(stream)

        # r1.delete()
        # r2.delete()
        # s1.delete()

        data = {}
        data['content'] = "placeholder"
        data['frequency'] = timedelta(days=1)
        data['start_date'] = date.today()
        data['end_date'] = date.today() + timedelta(days=1)
        data['recipients'] = [
            {'name': 'test', 'email_address': 'test@gmail.com'},
            {'name': 'test2', 'email_address': 'test2@gmail.com'}
        ]

        serializer = ScheduleSerializer(data=data)
        print(data)
        print(serializer.is_valid())
        print(serializer.errors)

        self.assertEqual(serializer.is_valid(), True)
        schedule = serializer.save()

        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Recipient.objects.count(), 2)
