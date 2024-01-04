import datetime

from django.contrib import admin
from django.db import models
from jsonfield import JSONField


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    place = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_start_date = models.DateField()
    registration_end_date = models.DateField()
    registration_open = models.BooleanField(default=False)  # F - zatvorena, T - otvorena
    is_active = models.BooleanField(default=False)  # ci je to aktualny event

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name

    @property
    def registrations_fits_today(self):
        return self.registration_start_date <= datetime.datetime.today().date() <= self.registration_end_date


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    primary_school = models.CharField(default=True)  # T - ZS, F - SS
    list_of_results = models.CharField(max_length=100)
    soccer = models.BooleanField(default=False)  # T - soccer, F - ne soccer
    group_size = models.IntegerField(default=4)
    advance = models.IntegerField(default=2)
    ranking_params = models.CharField(max_length=100)
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, null=True)
    results = JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields if field.name != "id"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields if field.name != "id"]


class Record(models.Model):
    team_name = models.CharField(max_length=100)
    order = models.CharField(max_length=100)


admin.site.register(Record)
admin.site.register(Event, EventAdmin)
admin.site.register(Category, CategoryAdmin)
