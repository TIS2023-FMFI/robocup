from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompetitorForm, SupervisorForm, TeamForm
from .models import Person, Team


def leader_panel(request):
    competitors = Person.objects.filter(_user_id=request.user.id, is_supervisor=False)
    supervisors = Person.objects.filter(_user_id=request.user.id, is_supervisor=True)
    teams = Team.objects.filter(_user_id=request.user.id)
    data = {"competitors": competitors, "supervisors": supervisors, "teams": teams}
    return render(request, "leader-panel.html", data)


def form_validation(form, request, html):
    if form.is_valid():
        form.save()
        messages.success(request, "The post has been updated successfully.")
        return render(request, f"{html}")
    else:
        messages.error(request, "Please correct the following errors:")
        return render(request, f"{html}", {"form": form})


def edit_competitor(request, id):
    post = get_object_or_404(Person, id=id)
    html = "competitors.html"

    if request.method == "GET":
        data = {"form": CompetitorForm(instance=post), "id": id}
        return render(request, f"{html}", data)

    elif request.method == "POST":
        form = CompetitorForm(request.POST, instance=post)
        form_validation(form, request, f"{html}")


def edit_supervisor(request, id):
    post = get_object_or_404(Person, id=id)
    html = "supervisors.html"

    if request.method == "GET":
        data = {"form": SupervisorForm(instance=post), "id": id}
        return render(request, f"{html}", data)

    elif request.method == "POST":
        form = SupervisorForm(request.POST, instance=post)
        return form_validation(form, request, f"{html}")


def edit_team(request, id):
    post = get_object_or_404(Person, id=id)
    html = "teams.html"

    if request.method == "GET":
        data = {"form": TeamForm(instance=post), "id": id}
        return render(request, f"{html}", data)

    elif request.method == "POST":
        form = TeamForm(request.POST, instance=post)
        return form_validation(form, request, f"{html}")


def team_assembly(request):
    context = {}
    if request.POST:
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = TeamForm()
    return render(request, "team_assembly.html", context)


def add_competitor(request):
    context = {}
    if request.POST:
        form = CompetitorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = CompetitorForm()
    return render(request, "add_competitor.html", context)


def add_supervisor(request):
    context = {}
    if request.POST:
        form = SupervisorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = SupervisorForm()
    return render(request, "add_supervisor.html", context)


def delete_competitor(request, id):
    competitor = Person.objects.get(id=id)
    html = "competitors.html"
    if request.method == "POST":
        competitor.delete()
    return render(request, f"{html}")


def delete_supervisor(request, id):
    supervisor = Person.objects.get(id=id)
    html = "supervisors.html"
    if request.method == "POST":
        supervisor.delete()
    return render(request, f"{html}")


def delete_team(request, id):
    team = Person.objects.get(id=id)
    html = "teams.html"
    if request.method == "POST":
        team.delete()
    return render(request, f"{html}")
