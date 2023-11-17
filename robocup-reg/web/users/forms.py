from django import forms
from django.contrib.auth.forms import BaseUserCreationForm

from web.users.models import User


class RegisterForm(BaseUserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class CustomLoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(label="Heslo", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form labels, if needed
        self.fields["email"].label = "Email"  # Change 'email' to 'username'
        self.fields["password"].label = "Password"

    def clean(self):
        if self.is_valid():
            self.cleaned_data["email"]
            self.cleaned_data["email"]
