from datetime import timedelta, date

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from schedules.models import Schedule, Recipient


class ScheduleModelTest(TestCase):
    def test_add_to_schedule_model(self):
        r1 = Recipient(email_address="test@test.com", name="test1")
        r2 = Recipient(email_address="test2@test.com", name="test2")

        r3 = Recipient.objects.create(
            email_address="test3@test.com",
            name="test3"
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
        self.assertEqual([r1, r2], list(s2.recipients.all()))
        self.assertNotEqual([r1, r3], list(s1.recipients.all()))

    def test_default_schedule_is_valid(self):
        s1 = Schedule()
        self.assertEqual(s1.content, '')
        self.assertEqual(s1.frequency, timedelta())

    def test_duplicate_schedule_is_invalid(self):
        start_date = date.today()
        end_date = start_date + timedelta(days=1)
        s1 = Schedule.objects.create(start_date=start_date, end_date=end_date)

        with self.assertRaises(ValidationError):
            s2 = Schedule(start_date=start_date, end_date=end_date)
            s2.full_clean()

    def test_stop_date_cannot_be_before_start_date(self):
        s1 = Schedule()
        s1.start_date = date.today()
        s1.end_date = s1.start_date - timedelta(days=5)
        with self.assertRaises(ValidationError):
            s1.save()

    def test_start_date_cannot_be_before_now(self):
        s1 = Schedule()
        s1.start_date = date.today() - timedelta(days=5)
        with self.assertRaises(ValidationError):
            s1.save()


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
