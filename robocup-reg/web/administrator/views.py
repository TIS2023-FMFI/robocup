from django.shortcuts import render


def admin_panel(request):
    return render(request, "admin-panel.html")
