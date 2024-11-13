from django.urls import path

"""
URL configuration for the 'myapp' Django application.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/
- The root URL ('') is routed to the `index` view.
- The 'about/' URL is routed to the `about` view.
- The 'about/<int:year>/' URL is routed to the `about` view with a year parameter.
- The 'about/<int:year>/<int:month>/' URL is routed to the `about` view with year and month parameters.
- The 'type/<int:type_no>/' URL is routed to the `detail` view with a type number parameter.
- The 'items/' URL is routed to the `ItemView` class-based view.
Namespace:
- app_name: "myapp"
"""
from . import views

app_name = "myapp"
urlpatterns = [
    # Index view
    path("", views.index, name="index"),
    # About view
    path("about/", views.AboutView.as_view(), name="about"),
    path("about/<int:year>/", views.AboutView.as_view(), name="about_year"),
    path(
        "about/<int:year>/<int:month>/",
        views.AboutView.as_view(),
        name="about_year_month",
    ),
    # Detail view
    path("<int:type_no>/", views.detail, name="detail"),
    # Items view
    path("items/", views.items, name="items"),
    # Lab group and member views
    path("lab-group/", views.LabGroupView.as_view(), name="lab_group"),
    path(
        "lab-member/<int:pk>/",
        views.LabMemberDetailView.as_view(),
        name="lab_member_detail",
    ),
    # Place order view
    path("placeorder/", views.placeorder, name="placeorder"),
]
