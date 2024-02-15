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
        fields = ["name", "primary_school", "list_of_results", "results", "detailed_pdf"]

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
    search_query.label = "Meno"


class JSONUploadForm(forms.Form):
    json_file = forms.FileField()


class BulkCheckInForm(forms.ModelForm):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={"readonly": "readonly"}))

    class Meta:
        model = Person
        fields = ["checked_in", "name"]


BulkCheckInFormSet = formset_factory(BulkCheckInForm, extra=0)


class EventToCopyFromForm(forms.Form):
    source_event = forms.ModelChoiceField(queryset=Event.objects.all())
    destination_event = forms.ModelChoiceField(queryset=Event.objects.all())


class StaffUserCreationForm(forms.Form):
    # email = forms.EmailField(label="Enter email of the new staff user")
    email = forms.EmailField(label="Email:")

    class Meta:
        fields = ["email"]
