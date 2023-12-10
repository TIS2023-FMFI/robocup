from django import forms
from django.contrib.auth.forms import BaseUserCreationForm

from web.leader.models import Person, Team


class RegisterFormCompetitor(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Person
        fields = ["email", "first_name", "last_nameb",
                  "phone_number",
                  "birth_date", "primary_school",
                  "diet", "accomodation1", "accomodation2",
                  "food1", "food2", "food3", "supervisor"]


class RegisterFormSupervisor(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Person
        fields = ["first_name", "last_name", "email",
                  "phone_number", "diet", "accomodation1",
                  "accomodation2", "food1", "food2", "food3"]


class RegisterFormTeam(BaseUserCreationForm):
    team_name = forms.CharField(required=True)

    class Meta:
        model = Team
        fields = ["team_name", "team_leader", "organization",
                  "categories", "competitors"]
