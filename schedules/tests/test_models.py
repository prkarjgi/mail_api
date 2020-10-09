from django.test import TestCase

from schedules.models import Schedule, Recipient, SchedRecip


class ScheduleModelTest(TestCase):
    def test_duplicates_are_invalid(self):
        pass

    def test_add_to_schedule_model(self):
        schedule = Schedule()

    def test_add_to_recipient_model(self):
        recipient = Recipient()

    def test_add_to_schedrecip_model(self):
        sched_recip = SchedRecip()
