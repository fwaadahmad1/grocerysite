from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Type(models.Model):
    """
    Type model represents a category or type of items in the grocery site.
    Attributes:
        name (CharField): The name of the type, with a maximum length of 200 characters.
    Methods:
        __str__(): Returns a string representation of the Type instance.
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return f"Type(name={self.name})"


class Item(models.Model):
    """
    Represents an item in the grocery store.
    Attributes:
        type (ForeignKey): A foreign key to the Type model, representing the category of the item.
        name (CharField): The name of the item, with a maximum length of 200 characters.
        price (DecimalField): The price of the item, with up to 10 digits and 2 decimal places.
        stock (PositiveIntegerField): The number of items in stock, defaulting to 100.
        available (BooleanField): A boolean indicating if the item is available, defaulting to True.
        description (TextField): A text field for the item's description, which can be null or blank.
        interested (PositiveIntegerField): The number of people interested in the item, defaulting to 0.
    Methods:
        __str__(): Returns a string representation of the item, including its name, type, price, stock, availability, and description.
    """

    type = models.ForeignKey(Type, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Item(name={self.name}, type={self.type.name}, price={self.price}, stock={self.stock}, available={self.available}, description={self.description})"

    def topup(self):
        self.stock += 50
        self.save()


class Client(User):
    """
    Client model that extends the User model.
    Attributes:
        CITY_CHOICES (list of tuple): List of tuples containing city choices.
        shipping_address (CharField): Shipping address of the client, can be null or blank.
        city (CharField): City of the client, chosen from CITY_CHOICES, defaults to "CH".
        interested_in (ManyToManyField): Types the client is interested in.
        phone_number (CharField): Phone number of the client, can be null or blank.
    Methods:
        __str__(): Returns a string representation of the Client instance, including username, shipping address, city, and interested types.
    """

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
    """
    OrderItem model represents an item in an order placed by a client.
    Attributes:
        ORDER_STATUS_CHOICES (list of tuple): Choices for the status of the order item.
        item (ForeignKey): Reference to the Item model.
        client (ForeignKey): Reference to the Client model.
        quantity (PositiveIntegerField): Quantity of the item ordered.
        status (IntegerField): Status of the order item, default is 1 (Placed).
        last_updated (DateTimeField): Timestamp of the last update to the order item.
    Methods:
        total_price(): Calculates the total price of the order item based on the item price and quantity.
        __str__(): Returns a string representation of the order item.
    """

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


class LabMember(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Other"),
        ],
        null=True,
        blank=True,
    )
    personal_page = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
