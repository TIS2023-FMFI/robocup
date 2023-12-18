from django.contrib import messages
from django.shortcuts import get_object_or_404, render

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

    if request.method == "GET":
        data = {"form": CompetitorForm(instance=post), "id": id}
        return render(request, "competitors.html", data)

    elif request.method == "POST":
        form = CompetitorForm(request.POST, instance=post)
        form_validation(form, request, "competitors.html")


def edit_supervisor(request, id):
    post = get_object_or_404(Person, id=id)

    if request.method == "GET":
        data = {"form": SupervisorForm(instance=post), "id": id}
        return render(request, "supervisors.html", data)

    elif request.method == "POST":
        form = SupervisorForm(request.POST, instance=post)
        return form_validation(form, request, "supervisors.html")


def edit_team(request, id):
    post = get_object_or_404(Person, id=id)

    if request.method == "GET":
        data = {"form": TeamForm(instance=post), "id": id}
        return render(request, "teams.html", data)

    elif request.method == "POST":
        form = TeamForm(request.POST, instance=post)
        return form_validation(form, request, "teams.html")
