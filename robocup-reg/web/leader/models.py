from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    leader_email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    birth_date = models.DateTimeField()
    primary_school = models.BooleanField()
    diet = models.CharField(default="Ziadna", max_length=1000)
    accomodation1 = models.BooleanField(default=True)
    accomodation2 = models.BooleanField(default=True)
    food1 = models.BooleanField(default=True)
    food2 = models.BooleanField(default=True)
    food3 = models.BooleanField(default=True)
    supervisor = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    leader_email = models.EmailField()
    team_name = models.CharField(max_length=100, unique=True)
    team_leader = models.IntegerField()
    organization = models.CharField(max_length=100)
    competitors = ArrayField(models.IntegerField())
    categories = ArrayField(models.IntegerField())  # v ktorych kategoriach tim sutazi
    category = models.BooleanField(default=True)  # T - ZS, F - SS


admin.site.register(Team)
admin.site.register(Person)
