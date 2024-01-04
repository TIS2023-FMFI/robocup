from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ..org.models import Category
from .forms import CompetitorForm, SupervisorForm, TeamForm
from .models import Person, Team


def leader_panel(request):
    competitors = Person.objects.filter(user_id=request.user.id, is_supervisor=False)
    supervisors = Person.objects.filter(user_id=request.user.id, is_supervisor=True)
    teams = Team.objects.filter(user_id=request.user.id)
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


def competitor_edit(request, id):
    instance = get_object_or_404(Person, id=id)
    html = "add_competitor.html"
    if request.method == "POST":
        form = CompetitorForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("leader_panel")
    else:
        form = CompetitorForm(instance=instance, user=request.user)

    return render(request, f"{html}", {"form": form})


def supervisor_edit(request, id):
    instance = get_object_or_404(Person, id=id)
    html = "add_supervisor.html"
    if request.method == "POST":
        form = SupervisorForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("leader_panel")
    else:
        form = SupervisorForm(instance=instance, user=request.user)

    return render(request, f"{html}", {"form": form})


def team_edit(request, id):
    instance = get_object_or_404(Team, id=id)
    html = "team_assembly.html"
    if request.method == "POST":
        form = TeamForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("leader_panel")
    else:
        form = TeamForm(instance=instance, user=request.user)

    return render(request, f"{html}", {"form": form})


def team_add(request):
    context = {}
    competitors = Person.objects.filter(is_supervisor=False, user=request.user)
    categories = Category.objects.all()
    context["competitors"] = competitors
    context["categories"] = categories
    if request.POST:
        form = TeamForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = TeamForm(user=request.user)
    return render(request, "team_assembly.html", context)


def competitor_add(request, user=None):
    context = {}
    if not user:
        user = request.user
    if request.POST:

        form = CompetitorForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = CompetitorForm(user=user)
    return render(request, "add_competitor.html", context)


def supervisor_add(request):
    context = {}
    if request.POST:
        form = SupervisorForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("leader_panel")
        else:
            context["form"] = form
    else:
        context["form"] = SupervisorForm(user=request.user)
    return render(request, "add_supervisor.html", context)


def competitor_delete(request, id):
    delete_person(id, request.user)
    return redirect(to="/leader-panel")


def supervisor_delete(request, id):
    delete_person(id, request.user)
    return redirect(to="/leader-panel")


def delete_person(id, user):
    supervisor = Person.objects.get(id=id)
    if user == supervisor.user:
        supervisor.delete()


def team_delete(request, id):
    team = Team.objects.get(id=id)
    team.delete()
    return redirect(to="/leader-panel")
