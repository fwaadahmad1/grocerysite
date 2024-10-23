from django.urls import path
from . import views

app_name = "myapp"
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("about/<int:year>/", views.about, name="about"),
    path("about/<int:year>/<int:month>/", views.about, name="about"),
    path("type/<int:type_no>/", views.detail, name="detail"),
    path('items/', views.ItemView.as_view(), name='items'),
]
