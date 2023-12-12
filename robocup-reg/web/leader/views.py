from django.shortcuts import render

from .models import Person, Team


def leader_panel(request):
    competitors = Person.objects.filter(_user_id=request.user.id, is_supervisor=False)
    supervisors = Person.objects.filter(_user_id=request.user.id, is_supervisor=True)
    teams = Team.objects.filter(_user_id=request.user.id)
    data = {"competitors": competitors, "supervisors": supervisors, "teams": teams}

    return render(request, "leader-panel.html", data)
