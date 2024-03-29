# Generated by Django 4.2.9 on 2024-01-23 10:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("org", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ("phone_number", models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ("birth_date", models.DateField(null=True)),
                ("primary_school", models.BooleanField(default=False)),
                ("diet", models.CharField(blank=True, default="", max_length=1000)),
                ("accomodation1", models.BooleanField(default=True)),
                ("accomodation2", models.BooleanField(default=True)),
                ("food1", models.BooleanField(default=True)),
                ("food2", models.BooleanField(default=True)),
                ("food3", models.BooleanField(default=True)),
                ("is_supervisor", models.BooleanField(default=False)),
                ("checked_in", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Person",
                "verbose_name_plural": "People",
            },
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("team_name", models.CharField(max_length=100, unique=True)),
                ("organization", models.CharField(max_length=100)),
                ("category", models.BooleanField(default=True)),
                ("categories", models.ManyToManyField(to="org.category")),
                ("competitors", models.ManyToManyField(to="leader.person")),
                (
                    "team_leader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="leader", to="leader.person"
                    ),
                ),
            ],
            options={
                "verbose_name": "Team",
                "verbose_name_plural": "Teams",
            },
        ),
    ]
