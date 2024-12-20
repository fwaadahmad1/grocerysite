# Generated by Django 5.1.2 on 2024-10-09 16:45

from django.db import migrations, models
from django.contrib.auth.models import User


city_map = {
    "Windsor": "WD",
    "Toronto": "TO",
    "Waterloo": "WL",
    "Chatham": "CH",
}

clients = [
    {
        "username": "usama",
        "password": "usama",
        "full_name": "Usama Mir",
        "address": "783 Dougall Avenue",
        "city": "Windsor",
        "interested_in": [1, 2, 3, 4, 5, 6],
    },
    {
        "username": "ziad",
        "password": "ziad",
        "full_name": "Ziad Kobti",
        "address": "456 Walker Avenue",
        "city": "Toronto",
        "interested_in": [1, 2, 3, 4],
    },
    {
        "username": "saja",
        "password": "saja",
        "full_name": "Saja Mansouri",
        "address": "789 Dominion Avenue",
        "city": "Waterloo",
        "interested_in": [4, 5, 6],
    },
    {
        "username": "prashanth",
        "password": "prashanth",
        "full_name": "Prashanth Ranga",
        "address": "123 Howard Avenue",
        "city": "Chatham",
        "interested_in": [2, 4],
    },
    {
        "username": "mark",
        "password": "mark",
        "full_name": "Mark Smith",
        "address": "791 Wyandotte Street",
        "city": "Windsor",
        "interested_in": [3, 4, 6],
    },
]


def create_clients(apps, schema_editor):
    Client = apps.get_model("myapp", "Client")

    for client_data in clients:
        client = Client(
            username=client_data["username"],
            first_name=client_data["full_name"].split()[0],
            last_name=client_data["full_name"].split()[1],
            shipping_address=client_data["address"],
            city=city_map[
                client_data["city"]
            ],  # Use the city map to get the correct value
        )
        client.save()


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_create_types"),
    ]
    operations = [migrations.RunPython(create_clients)]
