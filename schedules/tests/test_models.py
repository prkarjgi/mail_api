from datetime import timedelta, date

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from schedules.models import Schedule, Recipient, Interval
from utils.models import default_date_time


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

        s1 = Schedule(subject="test", content="test", frequency=timedelta())
        s1.save()
        s1.recipients.add(r1, r2)
        s2 = Schedule(
            subject="test", content="test", frequency=timedelta(hours=1)
        )
        s2.save()
        s2.recipients.add(r1, r2)
        self.assertEqual([r1, r2], list(s1.recipients.all()))
        self.assertEqual([r1, r2], list(s2.recipients.all()))
        self.assertNotEqual([r1, r3], list(s1.recipients.all()))

    def test_default_schedule_values_are_assigned(self):
        s1 = Schedule()
        self.assertEqual(s1.content, '')
        self.assertEqual(s1.frequency, timedelta())

    def test_default_schedule_is_valid(self):
        s1 = Schedule()
        s1.full_clean()
        s1.save()

    def test_duplicate_schedule_is_invalid(self):
        start_date = default_date_time()
        end_date = default_date_time(days=1)
        s1 = Schedule.objects.create(start_date=start_date, end_date=end_date)

        with self.assertRaises(ValidationError):
            s2 = Schedule(start_date=start_date, end_date=end_date)
            s2.full_clean()

    def test_stop_date_cannot_be_before_start_date(self):
        s1 = Schedule()
        s1.start_date = default_date_time()
        s1.end_date = s1.start_date - timedelta(days=5)
        # should raise error
        with self.assertRaises(ValidationError):
            s1.full_clean()

    def test_start_date_cannot_be_before_now(self):
        s1 = Schedule()
        s1.start_date = default_date_time(days=5, subtract=True)
        # should raise error
        with self.assertRaises(ValidationError):
            s1.full_clean()

    def test_save_method_performs_validation(self):
        s1 = Schedule()
        s1.start_date = default_date_time(days=2, subtract=True)
        with self.assertRaises(ValidationError):
            s1.save()

    def test_delete_schedule_cascades_to_map_table(self):
        s1 = Schedule(content="placeholder 1")
        s2 = Schedule(content="placeholder 2")

        r1 = Recipient.objects.create(email_address="test@gmail.com")
        r2 = Recipient.objects.create(email_address="test2@test.com")
        r3 = Recipient.objects.create(email_address="test3@gmil.com")

        s1.save()
        s2.save()

        s1.recipients.add(r1, r2)
        s2.recipients.add(r2, r3)

        self.assertEqual(r2.schedule_set.count(), 2)
        s1.delete()
        self.assertEqual(r2.schedule_set.count(), 1)
        s2.delete()
        self.assertEqual(r2.schedule_set.count(), 0)
        self.assertEqual(Recipient.objects.count(), 3)

    def test_frequency_greater_than_end_date_raises_validation_error(self):
        s1 = Schedule(
            content="placeholder",
            frequency=timedelta(days=5),
            end_date=default_date_time(),
            start_date=default_date_time(days=1)
        )
        with self.assertRaises(ValidationError):
            s1.full_clean()


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

    def test_email_address_is_validated(self):
        r1 = Recipient(email_address="test")
        with self.assertRaises(ValidationError):
            r1.full_clean()


class IntervalModelTest(TestCase):
    def test_create_interval_instance(self):
        i1 = Interval.objects.create(interval=timedelta(days=1))
        i2 = Interval.objects.create(interval=timedelta(hours=6))
        self.assertEqual(Interval.objects.count(), 2)

    def test_duplicate_interval_raises_validation_error(self):
        i1 = Interval.objects.create(interval=timedelta(days=1))
        with self.assertRaises(ValidationError):
            i2 = Interval(interval=timedelta(days=1))
            i2.full_clean()
