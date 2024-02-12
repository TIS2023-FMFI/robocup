from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import CustomLoginForm, RegisterForm

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = EmailMessage(
                "[rcj] Ucet vytvoreny",
                f"Dobrý deň!\n\nPráve ste si na stránkach robocup.skse.sk vytvorili\nnový účet s prihlasovacím e-mailom {user.email}.\n"
                 "Pokračujte ďalej zadaním všetkých dospelých členov\n"
                 "Vašej výpravy (dozor), potom zadaním všetkých\n"
                 "žiakov vo výprave - každému žiakovi nastavte, ktorý\n"
                 "dozor za neho zodpovedá. Potom povytvárajte jednotlivé\n"
                 "tímy a zaraďte žiakov do tímov a nastavte vedúcich tímov\n"
                 "vybratých zo sprievodných osôb a v ktorých kategóriách\n"
                 "budú jednotlivé tímy súťažiť: https://robocup.skse.sk/\n"
                 "\nV prípade ťažkostí alebo otázok sa neváhajte obrátiť\n"
                 "na organizátorov (kohut@skse.sk).\n\n"
                 "Tešíme sa na Vašu účasť!"
                 "\n\n(tento e-mail bol vygerovaný automaticky)",
                from_email="robocup@dai.fmph.uniba.sk",
                to=[user.email],
                reply_to=["kohut@skse.sk"],
            )
            email.send()
            send_mail("[rcj] nova registracia", f"zaregistroval sa: {user.email}",
                    from_email="robocup@dai.fmph.uniba.sk", 
                    recipient_list=["pavel.petrovic@gmail.com"])
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
            context["form"] = CustomLoginForm()
    else:
        context["form"] = CustomLoginForm()
    return render(request, "login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")
