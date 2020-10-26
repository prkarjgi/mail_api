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
        data = create_schedule_input_data(
            recipients=recipients
        )

        serializer = ScheduleSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        schedule = serializer.save()
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Recipient.objects.count(), 2)

    def test_serializer_can_serialize_queryset(self):
        recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'},
            {'name': 'test2', 'email_address': 'test2@gmail.com'}
        ]
        num_schedules = 10
        for iter in range(num_schedules):
            data = create_schedule_input_data(
                content=f"{iter}", recipients=recipients
            )
            serializer = ScheduleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

        schedules = Schedule.objects.all()
        serialized_schedules = ScheduleSerializer(
            instance=schedules, many=True
        )
        self.assertEqual(len(schedules), num_schedules)
        self.assertEqual(len(serialized_schedules.data), num_schedules)

    def test_recipient_duplication_raises_validation_error(self):
        recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'},
            {'name': 'test', 'email_address': 'test@gmail.com'}
        ]
        data = create_schedule_input_data(
            recipients=recipients
        )

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
        data = create_schedule_input_data(
            recipients=recipients
        )

        serializer = ScheduleSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            RECIPIENTS_GREATER_THAN_500_ERROR
        )
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_email_addresses_raise_validation_error(self):
        self.fail("Write test case for valid email addresses")

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

    def test_update_method_on_schedule_in_db(self):
        # self.fail("Write test case for updating schedule stored in the db")
        recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'}
        ]
        data = create_schedule_input_data(recipients=recipients)
        serializer = ScheduleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        self.assertEqual(Schedule.objects.count(), 1)

        recipients = [
            {'name': 'test', 'email_address': 'test1@gmail.com'}
        ]
        data = create_schedule_input_data(recipients=recipients)
        schedule = Schedule.objects.first()
        updated_serializer = ScheduleSerializer(instance=schedule, data=data)
        if updated_serializer.is_valid():
            updated_serializer.save()
        updated_schedule = Schedule.objects.first()
        updated_recipients = updated_schedule.recipients.all()

        self.assertEqual(
            updated_recipients[0].email_address,
            'test1@gmail.com'
        )


class RecipientSerializerTest(TestCase):
    def test_invalid_email_raises_validation_error(self):
        recipient = {'name': 'test', 'email_address': 'test'}
        recipient_serializer = RecipientSerializer(data=recipient)
        with self.assertRaises(ValidationError):
            recipient_serializer.is_valid(raise_exception=True)
