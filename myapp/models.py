from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Type(name={self.name})"


class Item(models.Model):
    type = models.ForeignKey(Type, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Item(name={self.name}, type={self.type.name}, price={self.price}, stock={self.stock}, available={self.available}, description={self.description})"


class Client(User):
    CITY_CHOICES = [
        ("WD", "Windsor"),
        ("TO", "Toronto"),
        ("CH", "Chatham"),
        ("WL", "Waterloo"),
    ]
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default="CH")
    interested_in = models.ManyToManyField(Type)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        interested_types = ", ".join(
            [str(type.name) for type in self.interested_in.all()]
        )
        return f"Client(username={self.username}, shipping_address={self.shipping_address}, city={self.city}, interested_in={interested_types})"


class OrderItem(models.Model):
    ORDER_STATUS_CHOICES = [
        (0, "Cancelled"),
        (1, "Placed"),
        (2, "Shipped"),
        (3, "Delivered"),
    ]

    item = models.ForeignKey(Item, related_name="order_items", on_delete=models.CASCADE)
    client = models.ForeignKey(
        Client, related_name="order_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    last_updated = models.DateTimeField(auto_now=True)

    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f"OrderItem(name={self.item.name}, quantity={self.quantity}, status={self.status}, client={self.client.username})"
