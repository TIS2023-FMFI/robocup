from django.shortcuts import render


def org_panel(request):
    return render(request, "org-panel.html")
