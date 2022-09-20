from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class MyWatchListResponseTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_url_html_exists(self):
        response = self.client.get(reverse("mywatchlist:show_watchlist_html"))
        self.assertEqual(response.status_code, 200)
    
    def test_url_json_exists(self):
        response = self.client.get(reverse("mywatchlist:show_watchlist_json"))
        self.assertEqual(response.status_code, 200)

    def test_url_xml_exists(self):
        response = self.client.get(reverse("mywatchlist:show_watchlist_xml"))
        self.assertEqual(response.status_code, 200)
