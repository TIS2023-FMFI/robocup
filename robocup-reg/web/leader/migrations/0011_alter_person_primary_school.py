# Generated by Django 4.2.8 on 2023-12-18 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leader", "0010_alter_person_birth_date_alter_person_diet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="primary_school",
            field=models.BooleanField(null=True),
        ),
    ]
