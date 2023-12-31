# Generated by Django 4.2.8 on 2023-12-05 18:22

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Person",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=100, unique=True)),
                ("phone_number", models.CharField(max_length=100, unique=True)),
                ("birth_date", models.DateTimeField()),
                ("primary_school", models.BooleanField()),
                ("diet", models.CharField(default="Ziadna", max_length=1000)),
                ("accomodation1", models.BooleanField(default=True)),
                ("accomodation2", models.BooleanField(default=True)),
                ("food1", models.BooleanField(default=True)),
                ("food2", models.BooleanField(default=True)),
                ("food3", models.BooleanField(default=True)),
                ("supervisor", models.CharField(max_length=100)),
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
                ("team_leader", models.IntegerField()),
                ("organization", models.CharField(max_length=100)),
                ("competitors", django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ("categories", django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ("category", models.BooleanField(default=True)),
            ],
        ),
    ]
