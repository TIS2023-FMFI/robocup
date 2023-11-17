from django import forms
from django.contrib.auth.forms import BaseUserCreationForm, AuthenticationForm

from web.users.models import RobocupUser


class RegisterForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = RobocupUser
        fields = ["email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = RobocupUser
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form labels, if needed
        self.fields['email'].label = 'Email'
        self.fields['password'].label = 'Password'

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        # Your custom validation logic here, e.g., checking if the user is active

        return self.cleaned_data