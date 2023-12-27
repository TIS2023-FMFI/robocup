# Generated by Django 4.2.8 on 2023-12-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leader", "0005_person_is_supervisor"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="team",
            options={"verbose_name": "Team", "verbose_name_plural": "Teams"},
        ),
        migrations.AlterField(
            model_name="person",
            name="phone_number",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
