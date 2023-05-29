# Generated by Django 4.1.5 on 2023-03-19 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="accepted",
            field=models.TextField(
                choices=[
                    ("Accepted", "Accepted"),
                    ("Denied", "Denied"),
                    ("Pending", "Pending"),
                ],
                default=("Pending", "Pending"),
            ),
        ),
    ]
