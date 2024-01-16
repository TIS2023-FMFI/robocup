from django import forms
from django.forms import formset_factory

from web.leader.models import Person
from web.org.models import Category, Event


class EventForm(forms.ModelForm):
    name = forms.CharField(required=True)
    place = forms.CharField(required=True)
    start_date = forms.DateTimeField(required=True)
    end_date = forms.DateTimeField(required=True)
    registration_start_date = forms.DateTimeField(required=True)
    registration_end_date = forms.DateTimeField(required=True)

    class Meta:
        model = Event
        fields = [
            "name",
            "place",
            "start_date",
            "end_date",
            "registration_start_date",
            "registration_end_date",
            "registration_open",
        ]


class CategoryForm(forms.ModelForm):
    name = forms.CharField(required=True)
    primary_school = forms.CharField(required=True)

    class Meta:
        model = Category
        fields = [
            "name",
            "primary_school",
            "list_of_results",
            "soccer",
            "group_size",
            "advance",
            "ranking_params",
            "results",
        ]

    def save(self, results, commit=True):
        instance = super(CategoryForm, self).save(commit=False)
        instance.results = results
        if commit:
            instance.save()
        return instance


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class ExpeditionLeaderForm(forms.Form):
    search_query = forms.CharField(max_length=255, required=False, label="Search")


class JSONUploadForm(forms.Form):
    json_file = forms.FileField()


class BulkCheckInForm(forms.ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={"readonly": "readonly"}))

    class Meta:
        model = Person
        fields = ["checked_in", "name"]


BulkCheckInFormSet = formset_factory(BulkCheckInForm, extra=0)


class EventToCopyFromForm(forms.Form):
    event = forms.ModelChoiceField(queryset=Event.objects.all())
