# Generated by Django 4.2.8 on 2023-12-18 09:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("org", "0002_alter_event_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="event",
            name="categories",
        ),
        migrations.AddField(
            model_name="category",
            name="event",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="org.event"),
        ),
    ]
