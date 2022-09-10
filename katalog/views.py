from django.shortcuts import render
from katalog.models import CatalogItem

# TODO: Create your views here.
def show_catalog(request):
    catalog = CatalogItem.objects.all()
    return render(
        request,
        "katalog.html",
        {
            "name": "Eduardus Tjitrahardja",
            "student_id": "2106653602",
            "catalogs": catalog,
        },
    )
