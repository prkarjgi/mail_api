from datetime import timedelta, date
from unittest import skip

from django.test import TestCase
from rest_framework.serializers import ValidationError

from schedules.serializers import ScheduleSerializer, RecipientSerializer
from schedules.models import Schedule, Recipient
from utils.testing import create_schedule_input_data, serialize_input_data
from utils.validators import RECIPIENTS_CONTAIN_DUPLICATES_ERROR,\
    RECIPIENTS_GREATER_THAN_500_ERROR, FIELDS_NOT_UNIQUE_TOGETHER_ERROR,\
    INVALID_EMAIL_ADDRESS_ERROR, END_DATE_NOT_ADDED_ERROR,\
    FREQUENCY_GREATER_THAN_END_DATE_ERROR
from utils.models import default_date_time


class ScheduleSerializerTest(TestCase):
    def setUp(self):
        self.recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'},
            {'name': 'test2', 'email_address': 'test2@gmail.com'}
        ]

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
        self.assertIsInstance(schedule, Schedule)
        self.assertEqual(Schedule.objects.count(), 1)
        self.assertEqual(Recipient.objects.count(), 2)

    def test_serializer_can_serialize_queryset(self):
        recipients = [
            {'name': 'test', 'email_address': 'test@gmail.com'},
            {'name': 'test2', 'email_address': 'test2@gmail.com'}
        ]
        num_schedules = 10
        serialize_input_data(
            recipients=recipients, num_schedules=num_schedules
        )
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
            {'name': 'test', 'email_address': f'test{idx}@test.com'}
            for idx in range(501)
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
        recipients = [
            {'name': 'test', 'email_address': 'test'},
            {'name': 'test', 'email_address': 'test@gmail.com'}
        ]
        data = create_schedule_input_data(recipients=recipients)
        schedule_serializer = ScheduleSerializer(data=data)

        self.assertEqual(schedule_serializer.is_valid(), False)
        self.assertEqual(
            schedule_serializer.errors['recipients'][0]['email_address'][0],
            INVALID_EMAIL_ADDRESS_ERROR
        )
        self.assertEqual(Schedule.objects.count(), 0)
        self.assertEqual(Recipient.objects.count(), 0)
        with self.assertRaises(ValidationError):
            schedule_serializer.is_valid(raise_exception=True)

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

    def test_update_schedule_recipients(self):
        serialize_input_data(recipients=self.recipients)
        self.assertEqual(Schedule.objects.count(), 1)
        recipients = [
            {'name': 'test', 'email_address': 'test1@gmail.com'}
        ]
        data = create_schedule_input_data(recipients=recipients)
        schedule = Schedule.objects.first()
        updated_serializer = ScheduleSerializer(instance=schedule, data=data)
        self.assertEqual(updated_serializer.is_valid(), True)
        updated_serializer.save()
        updated_recipients = schedule.recipients.all()

        self.assertEqual(
            updated_recipients[0].email_address,
            updated_serializer.data['recipients'][0]['email_address']
        )
        self.assertEqual(
            updated_recipients[0].email_address, 'test1@gmail.com'
        )

    def test_update_schedule_subject(self):
        serialize_input_data(recipients=self.recipients)
        self.assertEqual(Schedule.objects.count(), 1)

        data = create_schedule_input_data(subject="new subject")
        schedule = Schedule.objects.first()
        updated_serializer = ScheduleSerializer(instance=schedule, data=data)
        self.assertEqual(updated_serializer.is_valid(), True)
        updated_serializer.save()
        self.assertEqual(
            schedule.subject,
            updated_serializer.data['subject']
        )
        self.assertEqual(schedule.subject, "new subject")

    def test_update_schedule_content(self):
        serialize_input_data(recipients=self.recipients)
        self.assertEqual(Schedule.objects.count(), 1)

        data = create_schedule_input_data(content="new content")
        schedule = Schedule.objects.first()
        updated_serializer = ScheduleSerializer(instance=schedule, data=data)
        self.assertEqual(updated_serializer.is_valid(), True)
        updated_serializer.save()
        self.assertEqual(schedule.content, updated_serializer.data['content'])
        self.assertEqual(schedule.content, "new content")

    def test_update_frequency_gt_end_date_raises_validation_error(self):
        serialize_input_data(recipients=self.recipients)
        self.assertEqual(Schedule.objects.count(), 1)

        data = create_schedule_input_data(
            frequency=timedelta(days=5),
            end_date=default_date_time(days=1)
        )
        schedule = Schedule.objects.first()
        updated_serializer = ScheduleSerializer(instance=schedule, data=data)
        updated_serializer.is_valid()
        self.assertEqual(
            updated_serializer.errors['non_field_errors'][0],
            FREQUENCY_GREATER_THAN_END_DATE_ERROR
        )
        with self.assertRaises(ValidationError):
            updated_serializer.is_valid(raise_exception=True)

    def test_update_schedule_frequency(self):
        serialize_input_data(
            start_date=default_date_time(),
            end_date=default_date_time(days=5),
            recipients=self.recipients
        )
        self.assertEqual(Schedule.objects.count(), 1)

        data = create_schedule_input_data(
            frequency=timedelta(days=2),
            end_date=default_date_time(days=5)
        )
        schedule = Schedule.objects.first()
        updated_serializer = ScheduleSerializer(instance=schedule, data=data)
        self.assertEqual(updated_serializer.is_valid(), True)
        updated_serializer.save()
        self.assertEqual(
            updated_serializer.validated_data['frequency'], timedelta(days=2)
        )
        self.assertEqual(
            updated_serializer.validated_data['frequency'], schedule.frequency
        )

    def test_update_schedule_end_date_before_start_raises_error(self):
        serialize_input_data(recipients=self.recipients)
        schedule = Schedule.objects.first()
        new_data = create_schedule_input_data()
        new_data['start_date'] = new_data['end_date'] + timedelta(days=1)
        serializer = ScheduleSerializer(instance=schedule, data=new_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class RecipientSerializerTest(TestCase):
    def test_invalid_email_raises_validation_error(self):
        recipient = {'name': 'test', 'email_address': 'test'}
        recipient_serializer = RecipientSerializer(data=recipient)
        with self.assertRaises(ValidationError):
            recipient_serializer.is_valid(raise_exception=True)
