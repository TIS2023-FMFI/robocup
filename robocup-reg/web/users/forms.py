from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import BaseUserCreationForm

from web.users.models import RobocupUser


class RegisterForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = RobocupUser
        fields = ["email", "password1", "password2"]


class CustomLoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(label="Heslo", widget=forms.PasswordInput)

    class Meta:
        model = RobocupUser
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form labels, if needed
        self.fields["email"].label = "Email"  # Change 'email' to 'username'
        self.fields["password"].label = "Password"

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")

        return self.cleaned_data
