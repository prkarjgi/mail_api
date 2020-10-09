from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from schedules.models import Schedule, Recipient


class ScheduleModelTest(TestCase):
    def test_add_to_schedule_model(self):
        r1 = Recipient(
            email_address="test@test.com",
            name="test1"
        )
        r2 = Recipient(
            email_address="test2@test.com",
            name="test2"
        )
        r1.save()
        r2.save()

        s1 = Schedule(content="test", frequency=timedelta())
        s1.save()
        s1.recipients.add(r1, r2)

        s2 = Schedule(content="test", frequency=timedelta(1))
        s2.save()
        s2.recipients.add(r1, r2)

        self.assertEqual([r1, r2], list(s1.recipients.all()))

    def test_default_schedule_is_valid(self):
        s1 = Schedule()
        self.assertEqual(s1.content, '')
        self.assertEqual(s1.frequency, timedelta())

    def test_duplicate_schedule_is_invalid(self):
        s1 = Schedule.objects.create()
        with self.assertRaises(ValidationError):
            s2 = Schedule()
            s2.full_clean()


class RecipientModelTest(TestCase):
    def test_default_recipient_values(self):
        r1 = Recipient()
        self.assertEqual(r1.name, '')
        self.assertEqual(r1.email_address, 'dummy@placeholder.com')

    def test_default_recipient_is_valid(self):
        r1 = Recipient.objects.create()
        self.assertEqual(Recipient.objects.first(), r1)

    def test_duplicate_recipients_are_invalid(self):
        r1 = Recipient.objects.create()
        with self.assertRaises(ValidationError):
            r2 = Recipient()
            r2.full_clean()
