from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def results(request):
    return render(request, "results.html")


def leader_panel(request):
    return render(request, "leader_panel.html")
