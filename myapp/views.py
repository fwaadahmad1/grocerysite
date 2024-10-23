# Import necessary classes
from django.http import HttpResponse
from .models import Type, Item
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.views import View
from django.shortcuts import render


# Create your views here.
def index(request):
    type_list = Type.objects.all().order_by("id")
    item_list = Item.objects.all().order_by("-price")[:10]
    response = HttpResponse()
    heading1 = "<p>" + "Different Types: " + "</p>"
    response.write(heading1)
    for type in type_list:
        para = "<p>" + str(type.id) + ": " + str(type) + "</p>"
        response.write(para)
    heading2 = "<p>" + "Top 10 Most Expensive Items: " + "</p>"
    response.write(heading2)
    for item in item_list:
        para = (
            "<p>" + str(item.id) + ": " + str(item) + " - $" + str(item.price) + "</p>"
        )
        response.write(para)
    return response


def about(request, year=None, month=None):
    try:
        if year and month:
            date = datetime(year=int(year), month=int(month), day=1)
            formatted_date = date.strftime("%B, %Y")
            return HttpResponse(
                f"This is an Online Grocery Store. Date: {formatted_date}"
            )
        elif year:
            date = datetime(year=int(year), month=1, day=1)
            formatted_date = date.strftime("%Y")
            return HttpResponse(
                f"This is an Online Grocery Store. Year: {formatted_date}"
            )
        elif month:
            date = datetime(year=1, month=int(month), day=1)
            formatted_date = date.strftime("%B")
            return HttpResponse(
                f"This is an Online Grocery Store. Month: {formatted_date}"
            )
        else:
            return HttpResponse("This is an Online Grocery Store.")
    except ValueError:
        return HttpResponse("Invalid date format", status=400)


def detail(request, type_no):
    type_obj = get_object_or_404(Type, id=type_no)
    item_list = Item.objects.filter(type=type_obj).order_by("name")
    response = HttpResponse()
    heading = "<p>Items of type: " + str(type_obj) + "</p>"
    response.write(heading)
    for item in item_list:
        para = (
            "<p>"
            + str(item.id)
            + ": "
            + str(item.name)
            + " - $"
            + str(item.price)
            + "</p>"
        )
        response.write(para)
    return response


"""
The provided code shows the differences between FBV and CBV:
FBV:
Constructs HTML manually and writes it to the response.
Handles all logic within a single function.
CBV:
Uses a class with a get method to handle GET requests.
Utilizes render() to return an HTML template with context data.
This module contains views for a grocery site application.

ItemView(View):
    Handles GET requests to display a list of items using an HTML template.
"""


class ItemView(View):
    @staticmethod
    def get(request):
        # In CBV, we use class methods like get() to handle GET requests.
        # We use the render() function to return an HTML template with context data.
        items = Item.objects.all().order_by("name")
        return render(request, "items_list.html", {"items": items})
