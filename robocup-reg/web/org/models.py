from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    place = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_start_date = models.DateTimeField()
    registration_end_date = models.DateTimeField()
    registration_open = models.BooleanField(default=False)  # F - zatvorena, T - otvorena
    is_active = models.BooleanField(default=False)  # ci je to aktualny event
    categories = ArrayField(models.IntegerField())


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    primary_school = models.CharField(default=True)  # T - ZS, F - SS
    list_of_results = models.CharField(max_length=100)
    soccer = models.BooleanField(default=False)  # T - soccer, F - ne soccer
    group_size = models.IntegerField(default=4)
    advance = models.IntegerField(default=2)
    ranking_params = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


admin.site.register(Event)
admin.site.register(Category)
