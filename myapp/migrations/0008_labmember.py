# Generated by Django 5.1.2 on 2024-10-30 16:01

from django.db import migrations, models


def add_dummy_lab_members(apps, schema_editor):
    LabMember = apps.get_model("myapp", "LabMember")
    LabMember.objects.create(
        first_name="Fwaad",
        last_name="Ahmad",
        personal_page="http://example.com/fwaadahmad",
    )
    LabMember.objects.create(
        first_name="Asif",
        last_name="Lohar",
        personal_page="http://example.com/asiflohar",
    )
    LabMember.objects.create(
        first_name="Mohammad",
        last_name="Abdullah",
        personal_page="http://example.com/mohammadabdullah",
    )


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0007_populate_order_items"),
    ]

    operations = [
        migrations.CreateModel(
            name="LabMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("personal_page", models.URLField(blank=True)),
            ],
        ),
        migrations.RunPython(add_dummy_lab_members),
    ]