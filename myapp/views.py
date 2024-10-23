# Import necessary classes
from django.http import HttpResponse
from .models import Type, Item
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.views import View
from django.shortcuts import render


# Create your views here.
def index(request):
    """
    View function for the index page of the grocery site.

    This function retrieves all types and the top 10 most expensive items from the database,
    orders them, and constructs an HTTP response with this information formatted as HTML.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: An HTTP response containing the HTML representation of types and items.
    """
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
    """
    View function to display information about the online grocery store.

    This function constructs an HTTP response with information about the store and the formatted date,
    if provided. The date can be specified by year, month, or both. If an invalid date format is provided,
    a 400 Bad Request response is returned.

    Args:
        request (HttpRequest): The HTTP request object.
        year (int, optional): The year to be displayed. Defaults to None.
        month (int, optional): The month to be displayed. Defaults to None.

    Returns:
        HttpResponse: A response containing information about the store and the formatted date, if provided.
                      If both year and month are provided, the response includes the formatted month and year.
                      If only the year is provided, the response includes the year.
                      If only the month is provided, the response includes the month.
                      If neither is provided, a generic message about the store is returned.
                      If an invalid date format is provided, a 400 Bad Request response is returned.
    """
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
    """
    View function to display the details of items of a specific type.

    This function retrieves the type object based on the provided type number,
    filters the items by the type, and constructs an HTTP response with the list of items
    formatted as HTML.

    Args:
        request (HttpRequest): The HTTP request object.
        type_no (int): The ID of the type to filter items by.
    Returns:
        HttpResponse: An HTTP response containing the list of items of the specified type.
    """

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
differences between FBV and CBV:
FBV:
Constructs HTML manually and writes it to the response.
Handles all logic within a single function.
CBV:
Uses a class with a get method to handle GET requests.
Handles logic in separate methods within the class.
HTML template file (items_list.html) is used to render the list of items in a structured format.
Utilizes render() to return an HTML template with context data.
"""


class ItemView(View):
    """
    ItemView class handles the display of items in the grocery site.

    Methods:
        get(request):
            Handles GET requests to retrieve and display a list of items.
            Queries all items from the database, orders them by name, and renders the 'items_list.html' template with the items as context data.

    Attributes:
        None
    """

    @staticmethod
    def get(request):
        """
        Handles GET requests to retrieve and display a list of items.

        This method queries all items from the database, orders them by name, and renders the 'items_list.html' template with the items as context data.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: An HTTP response object containing the rendered HTML template with the list of items.
        """
        items = Item.objects.all().order_by("name")
        return render(request, "items_list.html", {"items": items})
