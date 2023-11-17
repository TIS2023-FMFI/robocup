from django.contrib.auth import authenticate, get_user_model, login, logout
from django.shortcuts import redirect, render

from .forms import CustomLoginForm, RegisterForm

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        redirect("home")

    if request.POST:
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
        else:
            context["login_form"] = form
    else:
        context["form"] = CustomLoginForm()
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")
