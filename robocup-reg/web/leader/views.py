from django.contrib import messages
from django.shortcuts import get_object_or_404, render

from .forms import CompetitorForm
from .models import Person, Team


def leader_panel(request):
    competitors = Person.objects.filter(_user_id=request.user.id, is_supervisor=False)
    supervisors = Person.objects.filter(_user_id=request.user.id, is_supervisor=True)
    teams = Team.objects.filter(_user_id=request.user.id)
    data = {"competitors": competitors, "supervisors": supervisors, "teams": teams}
    return render(request, "leader-panel.html", data)


def edit_competitor(request, id):
    post = get_object_or_404(Person, id=id)

    if request.method == "GET":
        data = {"form": CompetitorForm(instance=post), "id": id}
        return render(request, "competitors.html", data)

    elif request.method == "POST":
        form = CompetitorForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "The post has been updated successfully.")
            return render(request, "competitors.html")
        else:
            messages.error(request, "Please correct the following errors:")
            return render(request, "competitors.html", {"form": form})
