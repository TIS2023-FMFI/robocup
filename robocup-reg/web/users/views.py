from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from .models import RobocupUser
import logging

from .forms import RegisterForm, LoginForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "login.html", {"form": form})


def signin(request):
    if request.method == "POST":
        logging.debug("We are in")
        form = LoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print('pass')
        email = request.POST["username"]
        password = request.POST["password"]
        logging.debug(f"We are in {email}, {password}")
        user = authenticate(email, password)
        if user is not None:
            logging.debug(f"We are in {user}")
            login(request, user)
            return redirect("/home")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def authenticate(email=None, password=None):
    try:
        # Get the corresponding user.
        user = RobocupUser.objects.get(email=email)
        #  If password, matches just return the user. Otherwise, return None.
        if check_password(password, user.password):
            return user
        return None
    except RobocupUser.DoesNotExist:
        # No user was found.
        return None
