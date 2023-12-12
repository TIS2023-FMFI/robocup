from django import forms

from web.org.models import Event, Category


class EventForm(forms.Form):
    name = forms.CharField(required=True)
    place = forms.CharField(required=True)
    start_date = forms.DateTimeField(required=True)
    end_date = forms.DateTimeField(required=True)
    registration_start_date = forms.DateTimeField(required=True)
    registration_end_date = forms.DateTimeField(required=True)

    class Meta:
        model = Event
        fieldsets = ["name", "place", "start_date", "end_date",
                     "registration_start_date", "registration_end_date",
                     "registration_open", "categories"]


class CategoryForm(forms.Form):
    name = forms.CharField(required=True)
    primary_school = forms.CharField(required=True)

    class Meta:
        model = Category
        fieldsets = ["name", "primary_school", "list_of_results", "soccer",
                     "group_size", "advance", "ranking_params"]
