# Generated by Django 4.2.8 on 2023-12-18 14:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("leader", "0011_alter_person_primary_school"),
    ]

    operations = [
        migrations.RenameField(
            model_name="person",
            old_name="_user",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="team",
            old_name="_user",
            new_name="user",
        ),
    ]