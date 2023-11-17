from django.shortcuts import render


def leader_panel(request):
    return render(request, "leader-panel.html")
