# Generated by Django 5.1.2 on 2024-10-09 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_client_fullname_client_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(choices=[('WD', 'Windsor'), ('TO', 'Toronto'), ('CH', 'Chatham'), ('WL', 'Waterloo')], default='CH', max_length=2),
        ),
    ]
