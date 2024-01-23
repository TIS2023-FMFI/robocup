import csv

from django.shortcuts import HttpResponse, get_object_or_404, render

from ..leader.models import Person, Team
from ..org.forms import CSVImportForm
from ..org.models import Category, Event


def home(request):
    event = Event.objects.filter(is_active=True, registration_open=True)
    if event:
        data = {"open_event": event[0]}
        return render(request, "home.html", data)
    return render(request, "home.html")


def results(request, cat_id=None):
    teams = Team.objects.all()
    categories = Category.objects.all()
    if request.method == "POST":
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"].read().decode("utf-8").splitlines()
            csv_reader = csv.DictReader(csv_file)
            json_array = []
            all_team_names = Team.objects.values_list("team_name", flat=True)

            for row in csv_reader:
                if row["Tim"] in all_team_names:
                    json_array.append(row)
            instance = get_object_or_404(Category, id=cat_id)
            instance.results = json_array
            instance.save()

    else:
        form = CSVImportForm()
    data = {"teams": teams, "categories": categories.cat_id, "form": form}

    return render(request, "results.html", data)


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


def download_team_for_category(request, id):
    category = Category.objects.filter(id=id)
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="teamy_cat{category.get().name}.csv"'},
    )
    teamy = Team.objects.filter(categories=id)
    w = csv.writer(response)
    w.writerow(["nazov", "poriadie"])
    for t in teamy:
        w.writerow([t.team_name, 0])

    return response
