from django import forms

from web.org.models import Event, Category


class RegisterFormEvent(forms.Form):
    name = forms.CharField(required=True)
    place = forms.CharField(required=True)

    class Meta:
        model = Event
        fieldsets = ["name", "place", "start_date", "end_date",
                     "registration_start_date", "registration_end_date",
                     "registration_open", "categories"]


class RegisterFormCategory(forms.Form):
    name = forms.CharField(required=True)

    class Meta:
        model = Category
        fieldsets = ["name", "primary_school", "list_of_results", "soccer",
                     "group_size", "advance", "ranking_params"]
