# Generated by Django 5.1.2 on 2024-11-06 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_labmember_dob_labmember_email_labmember_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='interested',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
