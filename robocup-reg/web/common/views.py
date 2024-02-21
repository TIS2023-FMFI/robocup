import csv

from django.contrib import messages
from django.shortcuts import HttpResponse, render

from ..leader.models import Person, Team
from ..org.models import Category, Event


def home(request):
    event = Event.objects.filter(is_active=True, registration_open=True)
    if event:
        data = {"open_event": event[0]}
        return render(request, "home.html", data)
    return render(request, "home.html")


def results(request, id=1):
    teams = Team.objects.all()
    categories = Category.objects.filter(event__is_active=True)
    selected_category = categories.filter(id=id).get()
    result_dict = selected_category.results
    num_of_columns = len(result_dict[0].keys())
    teams_in_cat = set()
    ZS_teams = set()
    SS_teams = set()
    for team in teams:
        for elem in team.categories.all():
            if int(elem.id) == int(id):
                teams_in_cat.add(team)

    for team_ in teams_in_cat:
        zs = True
        for player in team_.competitors.all():
            if not player.primary_school:
                zs = False
        if not zs:
            SS_teams.add(team_.team_name)
        else:
            ZS_teams.add(team_.team_name)
    zoz = []
    ss_cat_res = []
    zs_cat_res = []
    if selected_category.list_of_results == "COMB":
        if result_dict:
            for i in range(1, len(result_dict) + 1):
                for prvok in result_dict:
                    if prvok["poradie"] == str(i):
                        if "body" in prvok.keys():
                            zoz.append([prvok["poradie"], prvok["nazov"], prvok["body"]])
                        else:
                            zoz.append([prvok["poradie"], prvok["nazov"]])
        else:
            messages.error(request, "Výsledky pre hľadanú kategóriu ešte neboli vyplnené.")

    elif selected_category.list_of_results == "SEPR":
        if result_dict:
            for i in range(1, len(result_dict) + 1):
                for prvok in result_dict:
                    if prvok["nazov"] in ZS_teams:
                        if prvok["poradie"] == str(i):
                            if "body" in prvok.keys():
                                zs_cat_res.append([prvok["poradie"], prvok["nazov"], prvok["body"]])
                            else:
                                zs_cat_res.append([prvok["poradie"], prvok["nazov"]])
                    else:
                        if prvok["poradie"] == str(i):
                            if "body" in prvok.keys():
                                ss_cat_res.append([prvok["poradie"], prvok["nazov"], prvok["body"]])
                            else:
                                ss_cat_res.append([prvok["poradie"], prvok["nazov"]])

    data = {
        "teams": teams,
        "categories": categories,
        "category_results": zoz,
        "selected_category": selected_category,
        "num_of_columns": num_of_columns,
        "ZS_teams": ZS_teams,
        "SS_teams": SS_teams,
        "zs_cat_res": zs_cat_res,
        "ss_cat_res": ss_cat_res,
    }

    return render(request, "results.html", data)


def info(request):
    teams = Team.objects.all()
    categories = Category.objects.filter(event__is_active=True)
    data = {"teams": teams, "categories": categories}
    return render(request, "info.html", data)


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


def detailed_results(request, id):
    return HttpResponse("TO BE IMPLEMENTED")
