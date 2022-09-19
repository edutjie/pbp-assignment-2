from django.urls import path
from mywatchlist.views import show_watchlist_html, show_watchlist_json, show_watchlist_xml

app_name = "mywatchlist"
urlpatterns = [
    path("html/", show_watchlist_html, name="show_watchlist_html"),
    path("json/", show_watchlist_json, name="show_watchlist_json"),
    path("xml/", show_watchlist_xml, name="show_watchlist_xml"),
]
