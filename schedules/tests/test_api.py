from datetime import timedelta, date
from unittest import skip

from django.test import TestCase
from rest_framework.serializers import ValidationError

from schedules.serializers import ScheduleSerializer, RecipientSerializer
from schedules.models import Schedule, Recipient
from utils.testing import create_schedule_input_data
from utils.validators import RECIPIENTS_CONTAIN_DUPLICATES_ERROR,\
    RECIPIENTS_GREATER_THAN_500_ERROR, FIELDS_NOT_UNIQUE_TOGETHER_ERROR


class ScheduleSerializerTest(TestCase):
    def test_serializer_can_deserialize_json(self):
        recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'},
            {'name': 'test2', 'email_address': 'test2@gmail.com'}
        ]
        data = create_schedule_input_data(recipients=recipients)

        serializer = ScheduleSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        schedule = serializer.save()
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Recipient.objects.count(), 2)

    def test_recipient_duplication_raises_validation_error(self):
        recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'},
            {'name': 'test', 'email_address': 'test@gmail.com'}
        ]
        data = create_schedule_input_data(recipients=recipients)

        serializer = ScheduleSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            RECIPIENTS_CONTAIN_DUPLICATES_ERROR
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_recipients_more_than_500_raises_validation_error(self):
        data = {}
        recipients = [
            {
                'name': 'test', 'email_address': f'test{idx}@test.com'
            } for idx in range(501)
        ]
        data = create_schedule_input_data(recipients=recipients)

        serializer = ScheduleSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            RECIPIENTS_GREATER_THAN_500_ERROR
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_email_raises_validation_error(self):
        pass

    def test_recipient_in_db_not_raises_validation_error(self):
        recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'}
        ]
        data_1 = create_schedule_input_data(
            content="placeholder 1",
            recipients=recipients
        )
        data_2 = create_schedule_input_data(
            content="placeholder 2",
            recipients=recipients
        )
        serializer_1 = ScheduleSerializer(data=data_1)
        serializer_2 = ScheduleSerializer(data=data_2)
        self.assertEqual(serializer_1.is_valid(), True)
        serializer_1.save()
        self.assertEqual(serializer_2.is_valid(), True)
        serializer_2.save()

    def test_schedule_unique_together_validation(self):
        recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'}
        ]
        data_1 = create_schedule_input_data(recipients=recipients)
        serializer_1 = ScheduleSerializer(data=data_1)
        serializer_1.is_valid()
        serializer_1.save()

        data_2 = create_schedule_input_data(recipients=recipients)
        serializer_2 = ScheduleSerializer(data=data_2)
        serializer_2.is_valid()
        self.assertEqual(
            serializer_2.errors['non_field_errors'][0],
            FIELDS_NOT_UNIQUE_TOGETHER_ERROR
        )
        with self.assertRaises(ValidationError):
            serializer_2.is_valid(raise_exception=True)
