from django.shortcuts import render

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
