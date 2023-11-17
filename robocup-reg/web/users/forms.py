from django import forms
from django.contrib.auth.forms import UserCreationForm

from web.users.models import RobocupUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = RobocupUser
        fields = ["email", "password1", "password2"]
