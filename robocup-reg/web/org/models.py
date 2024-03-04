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
    SCHOOLS = [("ZŠ", "Základná škola"), ("V", "Všetci")]
    RESULTS_LIST = [("BOTH", "Both"), ("COMB", "Combined"), ("SEPR", "Seperate")]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    primary_school = models.CharField(max_length=2, choices=SCHOOLS, default="ZŠ")  # T - ZS, F - SS
    list_of_results = models.CharField(choices=RESULTS_LIST, default="COMB", max_length=255)
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, null=True)
    results = JSONField(null=True, blank=True)
    detailed_pdf = models.FileField(null=True, blank=True, upload_to="uploads/%Y/%m/%d/")

    is_soccer = models.BooleanField(default=False)
    max_teams_per_group = models.IntegerField(default=0)
    advancing_teams_per_group = models.IntegerField(default=0)

    # pre_save kontrola
    def save(self, *args, **kwargs):
        if not self.is_soccer:
            self.max_teams_per_group = 0
            self.advancing_teams_per_group = 0
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        constraints = [models.UniqueConstraint(fields=["name", "event"], name="unique_name_event")]

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, data):
        name = data["fields"]["name"]
        primary_school = data["fields"]["primary_school"]
        list_of_results = data["fields"]["list_of_results"]
        event = data["fields"]["event"]

        results = data["fields"]["results"]

        is_soccer = data["fields"]["is_soccer"]
        max_teams_per_group = data["fields"].get("max_teams_per_group")
        advancing_teams_per_group = data["fields"].get("advancing_teams_per_group")

        return cls(
            name=name,
            primary_school=primary_school,
            list_of_results=list_of_results,
            event=Event.objects.filter(id=event).get(),

            results=results,

            is_soccer=is_soccer,
            max_teams_per_group=max_teams_per_group,
            advancing_teams_per_group=advancing_teams_per_group
        )


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
