# Import necessary classes
from django.http import HttpResponse
from .models import LabMember, Type, Item
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.views import View
from django.shortcuts import render
from django.views.generic import ListView, DetailView


# Create your views here.
def index(request):
    type_list = Type.objects.all().order_by("id")[:10]
    return render(request, "myapp/index.html", {"type_list": type_list})


class AboutView(View):
    def get(self, request, year=None, month=None):
        context = {}
        try:
            if year and month:
                date = datetime(year=int(year), month=int(month), day=1)
                context["formatted_date"] = date.strftime("%B, %Y")
                context["message"] = "This is an Online Grocery Store."
            elif year:
                date = datetime(year=int(year), month=1, day=1)
                context["formatted_date"] = date.strftime("%Y")
                context["message"] = "This is an Online Grocery Store."
            elif month:
                date = datetime(year=1, month=int(month), day=1)
                context["formatted_date"] = date.strftime("%B")
                context["message"] = "This is an Online Grocery Store."
            else:
                context["message"] = "This is an Online Grocery Store."
        except ValueError:
            context["message"] = "Invalid date format"
            return render(request, "myapp/about.html", context, status=400)

        return render(request, "myapp/about.html", context)


def detail(request, type_no):
    type_obj = get_object_or_404(Type, id=type_no)
    item_list = Item.objects.filter(type=type_obj).order_by("name")
    context = {"type": type_obj, "items": item_list}
    return render(request, "myapp/detail.html", context)


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


class LabGroupView(ListView):
    model = LabMember
    template_name = "myapp/lab_group.html"
    context_object_name = "lab_members"
    ordering = ["-first_name"]


class LabMemberDetailView(DetailView):
    model = LabMember
    template_name = "myapp/lab_member_detail.html"
    context_object_name = "lab_member"
