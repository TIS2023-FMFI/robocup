import csv

from django.shortcuts import HttpResponse, render

from ..leader.models import Person, Team
from ..org.models import Category, Event


def home(request):
    event = Event.objects.filter(is_active=True, registration_open=True)
    if event:
        data = {"open_event": event[0]}
        return render(request, "home.html", data)
    return render(request, "home.html")


def results(request, id=1):
    teams = Team.objects.all()
    categories = Category.objects.all()
    category_res = Category.objects.all().filter(id=id).values("results")
    data = {"teams": teams, "categories": categories, "category_results": category_res}
    return render(request, "results.html", data)


def info(request):
    teams = Team.objects.all()
    categories = Category.objects.all()
    data = {"teams": teams, "categories": categories}
    return render(request, "info.html", data)


def download_competitors(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="sutaziaci.csv"'},
    )

    sutaziaci = Person.objects.filter(is_supervisor=False)

    w = csv.writer(response)
    w.writerow(["meno", "priezvisko", "organizacia"])
    for s in sutaziaci:
        teamy = Team.objects.filter(competitors=s.id)
        org = ""
        if teamy:
            org = teamy[0].organization
        w.writerow([s.first_name, s.last_name, org])

    return response


def download_teams(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="teamy.csv"'},
    )

    teamy = Team.objects.all()

    w = csv.writer(response)
    w.writerow(["nazov", "organizacia", "rola", "meno"])
    for t in teamy:
        w.writerow([t.team_name, t.organization, "veduci", t.team_leader.first_name + " " + t.team_leader.last_name])
        for s in t.competitors.all():
            w.writerow(["", "", "clen", s.first_name + " " + s.last_name])

    return response
