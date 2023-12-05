from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import CustomLoginForm, RegisterForm, CSVImportForm
from .models import Record
import csv

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                "New registraton",
                f"A new registration was created under your name {user.email}.",
                from_email="robocup@thefilip.eu",
                recipient_list=[user.email],
            )
            login(request, user)
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

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


def import_csv(request):
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                Record.objects.create(
                    team_name=row['Meno tímu'],
                    order=row['Poradie']
                )

            # return redirect('success_page')  # Redirect to a success page
    else:
        form = CSVImportForm()

    return render(request, 'import.html', {'form': form})
