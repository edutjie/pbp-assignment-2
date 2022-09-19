from django.shortcuts import render
from mywatchlist.models import MyWatchList
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
watchlist = MyWatchList.objects.all()


def show_watchlist(request):
    return render(
        request,
        "mywatchlist.html",
        {
            "name": "Eduardus Tjitrahardja",
            "student_id": "2106653602",
            "watchlist": watchlist,
        },
    )


def show_watchlist_json(request):
    return HttpResponse(
        serializers.serialize("json", watchlist), content_type="application/json"
    )


def show_watchlist_xml(request):
    return HttpResponse(
        serializers.serialize("xml", watchlist), content_type="application/xml"
    )
