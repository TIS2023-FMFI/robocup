# Generated by Django 4.2.8 on 2023-12-12 14:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("org", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="event",
            options={"verbose_name": "Event", "verbose_name_plural": "Events"},
        ),
    ]
