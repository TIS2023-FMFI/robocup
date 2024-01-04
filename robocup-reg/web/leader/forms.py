import datetime

from django import forms
from django.core.exceptions import ValidationError

from web.leader.models import Person, Team


class CompetitorForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.DateField(
        required=True,
        widget=forms.SelectDateWidget(
            years=range(datetime.date.today().year - 20, datetime.date.today().year)
        ),  # Adjust the range as needed
    )
    supervisor = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Person
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "birth_date",
            "primary_school",
            "diet",
            "accomodation1",
            "accomodation2",
            "food1",
            "food2",
            "food3",
            "supervisor",
            # "checked_in"
        ]

    def __init__(self, *args, **kwargs):
        # Make user a keyword argument and pop it from kwargs
        user = kwargs.pop("user", None)
        super(CompetitorForm, self).__init__(*args, **kwargs)
        if user:
            self.user = user
            self.fields["supervisor"].queryset = Person.objects.filter(user_id=user.id, is_supervisor=True)
            self.fields["supervisor"].label = "Vyber dozorujúcu osobu"

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")

        if not email and not phone_number:
            raise ValidationError("Please provide either an email or a phone number.")

    def save(self, commit=True):
        instance = super(CompetitorForm, self).save(commit=False)
        instance.user = self.user  # Set the user field
        if commit:
            instance.save()
        return instance


class SupervisorForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Person
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "diet",
            "accomodation1",
            "accomodation2",
            "food1",
            "food2",
            "food3",
            # "checked_in"
        ]

    def __init__(self, *args, **kwargs):
        # Make user a keyword argument and pop it from kwargs
        user = kwargs.pop("user", None)
        super(SupervisorForm, self).__init__(*args, **kwargs)
        if user:
            self.user = user
            self.is_supervisor = True

    def save(self, commit=True):
        instance = super(SupervisorForm, self).save(commit=False)
        instance.user = self.user  # Set the user field
        instance.is_supervisor = self.is_supervisor
        if commit:
            instance.save()
        return instance


class TeamForm(forms.ModelForm):
    team_name = forms.CharField(required=True)
    organization = forms.CharField(required=True)

    class Meta:
        model = Team
        fields = ["team_name", "team_leader", "organization", "categories", "competitors"]

    def __init__(self, *args, **kwargs):
        # Make user a keyword argument and pop it from kwargs
        user = kwargs.pop("user", None)
        super(TeamForm, self).__init__(*args, **kwargs)
        if user:
            self.user = user
            self.fields["team_leader"].queryset = Person.objects.filter(user_id=user.id, is_supervisor=True)
            self.fields["team_leader"].label = "Vedúci tímu:"
            self.fields["competitors"].queryset = Person.objects.filter(user_id=user.id, is_supervisor=False)
            self.fields["competitors"].label = "Členovia tímu"
            self.fields["organization"].label = "Škola/Organizácia"
            self.fields["team_name"].label = "Názov tímu"
            self.fields["categories"].label = "Kategórie"

    def save(self, commit=True):
        instance = super(TeamForm, self).save(commit=False)
        instance.user = self.user  # Set the user field
        if commit:
            instance.save()
        self.save_m2m()
        return instance
