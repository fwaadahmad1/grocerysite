# Import necessary classes
from django.http import HttpResponse, HttpResponseRedirect
from .models import LabMember, Type, Item, OrderItem, Client
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from datetime import datetime
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def index(request):
    # Session counter
    if "index_count" in request.session:
        request.session["index_count"] += 1
    else:
        request.session["index_count"] = 1

    # Fetch the first 10 types ordered by id
    type_list = Type.objects.all().order_by("id")[:10]

    # Cookie setting
    response = render(request, "myapp/index.html", {"type_list": type_list})
    response.set_cookie("index_cookie", "index_value", max_age=10)
    return response


class AboutView(View):
    def get(self, request, year=None, month=None):
        # Session counter
        if "about_count" in request.session:
            request.session["about_count"] += 1
        else:
            request.session["about_count"] = 1

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

        # Cookie setting
        response = render(request, "myapp/about.html", context)
        response.set_cookie("about_cookie", "about_value", max_age=10)
        return response


def detail(request, type_no):
    # Session counter
    if "detail_count" in request.session:
        request.session["detail_count"] += 1
    else:
        request.session["detail_count"] = 1

    type_obj = get_object_or_404(Type, id=type_no)
    item_list = Item.objects.filter(type=type_obj).order_by("name")
    context = {"type": type_obj, "items": item_list}

    # Cookie setting
    response = render(request, "myapp/detail.html", context)
    response.set_cookie("detail_cookie", "detail_value", max_age=10)
    return response


class ItemView(View):
    @staticmethod
    def get(request):
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


def items(request):
    itemlist = Item.objects.all().order_by("id")[:20]
    return render(request, "myapp/items.html", {"itemlist": itemlist})


def placeorder(request):
    return render(request, "myapp/placeorder.html")


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "myapp/signup.html"
    success_url = reverse_lazy("myapp:login")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("myapp:index"))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details.")
    else:
        return render(request, "myapp/login.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(("myapp:index")))


@login_required(login_url="/login/")
def myorders(request):
    user = request.user
    if user.is_authenticated:
        if hasattr(user, "client"):
            client = user.client
            orders = OrderItem.objects.filter(client=client)
            return render(
                request, "myapp/myorders.html", {"orders": orders, "user": user}
            )
        else:
            return HttpResponse("You are not a registered client!")
    else:
        return HttpResponse("You are not authenticated!")
