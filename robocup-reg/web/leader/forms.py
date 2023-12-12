from django import forms
from django.contrib.auth.forms import BaseUserCreationForm

from web.leader.models import Person, Team


class CompetitorForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    birth_date = forms.CharField(required=True)

    class Meta:
        model = Person
        fields = ["email", "first_name", "last_nameb",
                  "phone_number",
                  "birth_date", "primary_school",
                  "diet", "accomodation1", "accomodation2",
                  "food1", "food2", "food3", "supervisor"]


class SupervisorForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = Person
        fields = ["first_name", "last_name", "email",
                  "phone_number", "diet", "accomodation1",
                  "accomodation2", "food1", "food2", "food3"]


class TeamForm(forms.Form):
    team_name = forms.CharField(required=True)
    team_leader = forms.CharField(required=True)
    organization = forms.CharField(required=True)
    categories = forms.CharField(required=True)
    competitors = forms.CharField(required=True)

    class Meta:
        model = Team
        fields = ["team_name", "team_leader", "organization",
                  "categories", "competitors"]
