from django.test import TestCase
from django.test import Client

# Create your tests here.
class MyWatchListResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url_json_exists(self):
        response = self.client.get("/mywatchlist/json/")
        self.assertEqual(response.status_code, 200)

    def test_url_xml_exists(self):
        response = self.client.get("/mywatchlist/xml/")
        self.assertEqual(response.status_code, 200)
