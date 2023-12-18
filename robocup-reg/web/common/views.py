import csv

from django.shortcuts import HttpResponse, render

from ..leader import models as leader_models
from ..org import models as org_models


def home(request):
    event = org_models.Event.objects.filter(is_active=True, registration_open=True)
    if event:
        data = {"open_event": event[0]}
        return render(request, "home.html", data)
    return render(request, "home.html")


def results(request):
    return render(request, "results.html")


def leader_panel(request):
    return render(request, "leader_panel.html")


def download_competitors(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="sutaziaci.csv"'},
    )

    sutaziaci = leader_models.Person.objects.filter(is_supervisor=False)

    w = csv.writer(response)
    w.writerow(["meno", "priezvisko"])
    for s in sutaziaci:
        w.writerow([s.first_name, s.last_name])

    return response
