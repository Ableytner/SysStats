from django.test import TestCase, Client
from django.contrib.auth.models import User

import os

from stats.models import Record, RamRecord, DriveRecord, NetworkRecord

USERNAME = "testuser"
PASSWORD = "12345"
STATIC_FOLDER = os.path.join(os.getcwd(), "sysstats", "stats", "static")
if not os.path.isdir(STATIC_FOLDER):
    STATIC_FOLDER = os.path.join(os.getcwd(), "stats", "static")

class AnimalTestCase(TestCase):
    def setUp(self):
        # create testuser
        user = User.objects.create(username=USERNAME)
        user.set_password(PASSWORD)
        user.save()

        # test record creation
        RamRecord.objects.create(ram_usage=102301, ram_total=201353).save()
        DriveRecord.objects.create(drive_usage=433432, total_drive_size=471342, drive_change=10341).save()
        NetworkRecord.objects.create(network_up=42421, network_down=24551, network_up_total=121242, network_down_total=211145).save()
        Record(cpu_usage=27, ram_usage=RamRecord.objects.last(), drive_usage=DriveRecord.objects.last(), network_usage=NetworkRecord.objects.last()).save()

        record = Record.objects.last()
        self.assertEqual(record.ram_usage.ram_usage, 102301)
        self.assertEqual(record.ram_usage.ram_total, 201353)
        self.assertEqual(record.drive_usage.drive_usage, 433432)
        self.assertEqual(record.drive_usage.total_drive_size, 471342)
        self.assertEqual(record.drive_usage.drive_change, 10341)
        self.assertEqual(record.network_usage.network_up, 42421)
        self.assertEqual(record.network_usage.network_down, 24551)
        self.assertEqual(record.network_usage.network_up_total, 121242)
        self.assertEqual(record.network_usage.network_down_total, 211145)
        self.assertEqual(record.cpu_usage, 27)

    def test_index_redirect(self):
        c = Client()
        response = c.post("/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], "/accounts/login/?next=/")
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_history_redirect(self):
        c = Client()
        response = c.post("/history/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertEqual(response.redirect_chain[0][0], "/accounts/login/?next=/history/")
        self.assertEqual(response.redirect_chain[0][1], 302)

    def test_login(self):
        c = Client()
        self._login(c)
    
    def test_index(self):
        c = Client()
        self._login(c)
        response = c.post("/")
        self.assertEqual(response.status_code, 200)

        # check if the diagram files got created
        self.assertTrue(os.path.isfile(os.path.join(STATIC_FOLDER, "images", "cpu_usage_pie.png")))
        self.assertTrue(os.path.isfile(os.path.join(STATIC_FOLDER, "images", "drive_usage_pie.png")))
        self.assertTrue(os.path.isfile(os.path.join(STATIC_FOLDER, "images", "ram_usage_pie.png")))

    def test_history(self):
        c = Client()
        self._login(c)
        response = c.post("/history/")
        self.assertEqual(response.status_code, 200)

        # check if the diagram files got created
        self.assertTrue(os.path.isfile(os.path.join(STATIC_FOLDER, "images", "cpu_usage_histogram.png")))
        self.assertTrue(os.path.isfile(os.path.join(STATIC_FOLDER, "images", "drive_usage_histogram.png")))
        self.assertTrue(os.path.isfile(os.path.join(STATIC_FOLDER, "images", "network_upload_histogram.png")))
        self.assertTrue(os.path.isfile(os.path.join(STATIC_FOLDER, "images", "network_download_histogram.png")))
        self.assertTrue(os.path.isfile(os.path.join(STATIC_FOLDER, "images", "ram_usage_histogram.png")))

    def _login(self, c: Client):
        logged_in = c.login(username=USERNAME, password=PASSWORD)
        self.assertTrue(logged_in)
