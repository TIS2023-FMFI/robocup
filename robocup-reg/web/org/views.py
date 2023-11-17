from django.shortcuts import render


def org_panel(request):
    return render(request, "org-panel.html")


def check_in(request):
    return render(request, "check_in.html")


def categories(request):
    return render(request, "categories.html")
