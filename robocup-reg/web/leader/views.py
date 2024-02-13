from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render

from ..org.models import Category, Event
from ..users.models import RobocupUser
from .forms import CompetitorForm, SupervisorForm, TeamForm
from .models import Person, Team


@login_required
def leader_panel(request):
    event = Event.objects.filter(is_active=True, registration_open=True)
    if not event.exists() and not request.user.is_staff:
        messages.error(request, "Neexistuje event na ktorý je možné sa registrovať.")
        return redirect("home")
    competitors = Person.objects.filter(user_id=request.user.id, is_supervisor=False)
    supervisors = Person.objects.filter(user_id=request.user.id, is_supervisor=True)
    teams = Team.objects.filter(user_id=request.user.id)
    data = {"competitors": competitors, "supervisors": supervisors, "teams": teams}
    return render(request, "leader-panel.html", data)


@login_required
def competitor_edit(request, id):
    instance = get_object_or_404(Person, id=id)
    html = "add_competitor.html"
    if request.method == "POST":
        form = CompetitorForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            obj = form.save()
            send_alert(request.user, obj, "zmenene udaje sutaziaceho")
            messages.success(request, "Zmeny boli uložené.")
            return redirect("leader_panel")
    else:
        form = CompetitorForm(instance=instance, user=request.user)

    return render(request, f"{html}", {"form": form})


@login_required
def supervisor_edit(request, id):
    instance = get_object_or_404(Person, id=id)
    html = "add_supervisor.html"
    if request.method == "POST":
        form = SupervisorForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            obj = form.save()
            send_alert(request.user, obj, "zmenene udaje doprevadzajucej osoby")
            messages.success(request, "Zmeny boli uložené.")
            return redirect("leader_panel")
    else:
        form = SupervisorForm(instance=instance, user=request.user)

    return render(request, f"{html}", {"form": form})


@login_required
def team_edit(request, id):
    instance = get_object_or_404(Team, id=id)
    html = "team_assembly.html"
    if request.method == "POST":
        form = TeamForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            team = form.save()
            for person in team.competitors.all():
                if not person.primary_school:
                    team.category = False
                    team.save()
                    break
            send_alert(request.user, team, "zmenene udaje o time (kategorie/ucastnikov/nazov/team leader...)")
            messages.success(request, "Zmeny boli uložené.")
            return redirect("leader_panel")
    else:
        form = TeamForm(instance=instance, user=request.user)
        initial_team_leader = instance.team_leader
        initial_competitors = instance.competitors.all()
        initial_categories = instance.categories.all()

        form.fields["team_leader"].initial = initial_team_leader
        form.fields["competitors"].initial = initial_competitors
        form.fields["categories"].initial = initial_categories
    return render(request, f"{html}", {"form": form})


@login_required
def team_add(request, id=None):
    context = {}
    user = request.user
    if id:
        user = RobocupUser.objects.filter(id=id).get()
        context["id"] = id
    competitors = Person.objects.filter(is_supervisor=False, user=user)
    if not Person.objects.filter(user=user.id, is_supervisor=True).exists() or not competitors.exists():
        messages.error(request, "Pre vytvorenie tímu je potrebné najprv vytvoriť dozor a súťažiacich.")
        return redirect("leader_panel")
    categories = Category.objects.all()
    context["competitors"] = competitors
    context["categories"] = categories
    if request.POST:
        form = TeamForm(request.POST, user=user)
        if form.is_valid():
            team = form.save()
            for person in team.competitors.all():
                if not person.primary_school:
                    team.category = False
                    team.save()
                    break
            send_alert(user, team, "pridany novy tim")
            messages.success(request, "Tím bol pridaný.")
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = TeamForm(user=user)
    return render(request, "team_assembly.html", context)


@login_required
def competitor_add(request, id=None):
    context = {}
    user = request.user
    if id:
        user = RobocupUser.objects.filter(id=id).get()
        context["id"] = id
    if not Person.objects.filter(user=user.id, is_supervisor=True).exists():
        messages.error(request, "Pre vytvorenie súťažiaceho je potrebné najprv vytvoriť dozor.")
        return redirect("leader_panel")
    if request.POST:
        form = CompetitorForm(request.POST, user=user)
        if form.is_valid():
            obj = form.save()
            send_alert(user, obj, "pridany novy sutaziaci")
            messages.success(request, "Súťažiaci bol pridaný.")
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = CompetitorForm(user=user)
    return render(request, "add_competitor.html", context)


@login_required
def supervisor_add(request, id=None):
    context = {}
    user = request.user
    if id:
        user = RobocupUser.objects.filter(id=id).get()
        context["id"] = id
    if request.POST:
        form = SupervisorForm(request.POST, user=user)
        if form.is_valid():
            obj = form.save()
            send_alert(user, obj, "pridana nova sprievodna osoba")
            messages.success(request, "Dozor bol pridaný.")
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = SupervisorForm(user=user)
    return render(request, "add_supervisor.html", context)


@login_required
def competitor_delete(request, id):
    if delete_person(id, request.user):
        messages.success(request, "Súťažiaci bol odstánený.")
        return redirect(to="/leader-panel")


@login_required
def supervisor_delete(request, id):
    if delete_person(id, request.user):
        messages.success(request, "Dozor bol odstánený.")
        return redirect(to="/leader-panel")


@login_required
def team_delete(request, id):
    team = Team.objects.get(id=id)
    if request.user == team.user:
        send_alert(request.user, team, "tim zmazany")
        team.delete()
        messages.success(request, "Tím bol odstánený.")

        return redirect(to="/leader-panel")


def delete_person(id, user):
    supervisor = Person.objects.get(id=id)
    if user == supervisor.user:
        send_alert(user, supervisor, "clen timu zmazany")
        supervisor.delete()
        return True
    return False


def form_validation(form, request, html):
    if form.is_valid():
        form.save()
        messages.success(request, "The post has been updated successfully.")
        return render(request, f"{html}")
    else:
        messages.error(request, "Please correct the following errors:")
        return render(request, f"{html}", {"form": form})


def send_alert(user, instance, change):
    event = Event.objects.filter(is_active=True, registration_open=True)
    if event:
        event = event[0]
        if not event.registrations_fits_today:
            email = EmailMessage(
                "[rcj] Zmena v registracii po datume",
                f"""Pouzivatel {user.email} vykonal zmenu po skonceni registracie:\n\n{change}\n\nnovy/upraveny udaj:\n\n{instance}.
                """,
                from_email="robocup@dai.fmph.uniba.sk",
                to=["pavel.petrovic@gmail.com"],
            )
            email.send()
