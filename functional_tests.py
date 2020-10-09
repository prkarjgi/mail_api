from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewScheduleTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_add_new_schedule(self):
        # the user goes to the home page of the app
        self.browser.get(self.live_server_url)

        # they see a button to add a new schedule
        # they see form entries to add a new schedule

        # they enter two email addresses to the recipients list

        # they add some content to be put in the mails

        # they enter the scheduling frequency - once a day at 8:00 am IST

        # they hit enter and see the url change and show them the new schedule
        # added

        # they are happy and close the browser
        self.fail("Add to FT")
