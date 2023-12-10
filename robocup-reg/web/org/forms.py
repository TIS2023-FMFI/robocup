from django import forms

from web.org.models import Event, Category


class RegisterFormEvent(forms.Form):

    class Meta:
        model = Event
        fieldsets = ["name", "place", "start_date", "end_date",
                     "registration_start_date", "registration_end_date",
                     "registration_open", "categories"]
