from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models

from ..users import models as user_models


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    _user = models.ForeignKey(to=user_models.User, on_delete=models.CASCADE)
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
    is_supervisor = models.BooleanField(default=False)
    supervisor = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    _user = models.ForeignKey(to=user_models.User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=100, unique=True)
    team_leader = models.IntegerField()
    organization = models.CharField(max_length=100)
    competitors = ArrayField(models.IntegerField())
    categories = ArrayField(models.IntegerField())  # v ktorych kategoriach tim sutazi
    category = models.BooleanField(default=True)  # T - ZS, F - SS

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"

    def __str__(self):
        return self.team_name


class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Person._meta.fields if field.name != "id"]


class TeamAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Team._meta.fields if field.name != "id"]


admin.site.register(Team, TeamAdmin)
admin.site.register(Person, PersonAdmin)
