from unittest import skip
from datetime import timedelta
from io import BytesIO

from django.test import TestCase
from django.urls import resolve
from rest_framework.parsers import JSONParser


from schedules.views import schedule_list, schedule_one
from schedules.serializers import ScheduleSerializer
from schedules.models import Schedule, Recipient

from utils.testing import create_schedule_input_data, serialize_input_data


class ScheduleViewTest(TestCase):
    def setUp(self):
        self.schedule_base_url = "/api/schedules/"
        self.recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'},
            {'name': 'test2', 'email_address': 'test2@test.com'}
        ]
        return super().setUp()

    def test_get_schedule_list(self):
        recipients = self.recipients
        num_schedules = 5
        serialize_input_data(
            num_schedules=num_schedules, recipients=recipients
        )

        response = self.client.get(self.schedule_base_url)
        bytes_stream = BytesIO(response.content)
        response_json = JSONParser().parse(bytes_stream)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_json), num_schedules)

    def test_post_new_schedule(self):
        recipients = self.recipients
        data = create_schedule_input_data(recipients=recipients)

        response = self.client.post(
            path=self.schedule_base_url,
            data=data,
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Recipient.objects.count(), 2)

        frequency = Schedule.objects.first().frequency
        self.assertIsInstance(frequency, timedelta)

    def test_get_schedule(self):
        serialize_input_data(recipients=self.recipients, num_schedules=5)

        response_1 = self.client.get(path=f'{self.schedule_base_url}1/')
        self.assertEqual(response_1.status_code, 200)

        response_2 = self.client.get(path=f'{self.schedule_base_url}2/')
        self.assertEqual(response_2.status_code, 200)

    def test_update_one_schedule(self):
        recipients = self.recipients
        data = create_schedule_input_data(recipients=recipients)

        response = self.client.post(
            path=self.schedule_base_url,
            data=data,
            content_type="application/json"
        )
        print(response.content)

        data = create_schedule_input_data(content="new content")
        update_response = self.client.put(
            path=f'{self.schedule_base_url}1/',
            data=data,
            content_type="application/json"
        )
        print(update_response.content)

    def test_update_schedule_with_invalid_data(self):
        self.fail("Write unit test to update a schedule with invalid data")

    def test_delete_schedule(self):
        serialize_input_data(recipients=self.recipients)
        schedule = Schedule.objects.all()

        response = self.client.delete(path=f'{self.schedule_base_url}1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Schedule.objects.count(), 0)
        self.assertEqual(
            Recipient.objects.count(), len(self.recipients)
        )
        self.assertEqual(
            len(Schedule.recipients.through.objects.all()), 0
        )
