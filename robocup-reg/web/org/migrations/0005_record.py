# Generated by Django 4.2.8 on 2023-12-21 16:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("org", "0004_alter_event_end_date_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Record",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("team_name", models.CharField(max_length=100)),
                ("order", models.CharField(max_length=100)),
            ],
        ),
    ]
