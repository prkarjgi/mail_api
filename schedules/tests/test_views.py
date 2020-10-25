from django.test import TestCase
from django.urls import resolve
from unittest import skip

from schedules.views import add_schedule


class ScheduleAddTest(TestCase):
    @skip
    def test_add_one_schedule(self):
        self.client.get("/schedules/add")

    @skip
    def test_add_schedule_resolves_to_add_view(self):
        add = resolve("/schedules/add")
        self.assertEqual(add.func, add_schedule)
