# Generated by Django 4.2.8 on 2023-12-18 13:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leader", "0009_alter_person_birth_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="birth_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="diet",
            field=models.CharField(default="", max_length=1000),
        ),
    ]
