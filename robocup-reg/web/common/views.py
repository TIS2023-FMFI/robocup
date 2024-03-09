import csv
import json

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponse, redirect, render

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

    teams_in_cat = set()
    ZS_teams = set()
    SS_teams = set()

    num_of_columns = 0
    group_results = {}
    zoz = []
    ss_cat_res = []
    zs_cat_res = []

    # ak to neni soccer
    if not selected_category.is_soccer:

        if result_dict is None:
            result_dict = dict()
            num_of_columns = 0
        else:
            num_of_columns = len(result_dict[0].keys())

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
                zs_poradie = 1
                ss_poradie = 1
                for i in range(1, len(result_dict) + 1):
                    for prvok in result_dict:
                        if prvok["nazov"] in ZS_teams:
                            if prvok["poradie"] == str(i):
                                if "body" in prvok.keys():
                                    zs_cat_res.append([zs_poradie, prvok["nazov"], prvok["body"]])
                                else:
                                    zs_cat_res.append([zs_poradie, prvok["nazov"]])
                                zs_poradie += 1
                        else:
                            if prvok["poradie"] == str(i):
                                if "body" in prvok.keys():
                                    ss_cat_res.append([ss_poradie, prvok["nazov"], prvok["body"]])
                                else:
                                    ss_cat_res.append([ss_poradie, prvok["nazov"]])
                                ss_poradie += 1
            else:
                messages.error(request, "Výsledky pre hľadanú kategóriu ešte neboli vyplnené.")
        else:
            if result_dict:
                for i in range(1, len(result_dict) + 1):
                    for prvok in result_dict:
                        if prvok["poradie"] == str(i):
                            if "body" in prvok.keys():
                                zoz.append([prvok["poradie"], prvok["nazov"], prvok["body"]])
                            else:
                                zoz.append([prvok["poradie"], prvok["nazov"]])
                zs_poradie = 1
                ss_poradie = 1
                for i in range(1, len(result_dict) + 1):
                    for prvok in result_dict:
                        if prvok["nazov"] in ZS_teams:
                            if prvok["poradie"] == str(i):
                                if "body" in prvok.keys():
                                    zs_cat_res.append([zs_poradie, prvok["nazov"], prvok["body"]])
                                else:
                                    zs_cat_res.append([zs_poradie, prvok["nazov"]])
                                zs_poradie += 1
                        else:
                            if prvok["poradie"] == str(i):
                                if "body" in prvok.keys():
                                    ss_cat_res.append([ss_poradie, prvok["nazov"], prvok["body"]])
                                else:
                                    ss_cat_res.append([ss_poradie, prvok["nazov"]])
                                ss_poradie += 1
            else:
                messages.error(request, "Výsledky pre hľadanú kategóriu ešte neboli vyplnené.")

    # ak to je soccer
    elif selected_category.is_soccer:
        if result_dict:
            result_dict = json.loads(selected_category.results)
            # Assuming result_dict is structured with group keys and match results
            for group, matches in result_dict.items():
                teams_stats = {}
                for match_teams, match_result in matches.items():
                    # print(f"match_result: {match_result}")
                    team_a, team_b = match_teams.split("-")[0:2]
                    # Initialize or update team stats
                    for team in [team_a, team_b]:
                        if team not in teams_stats:
                            teams_stats[team] = {"P": 0, "S": [0, 0], "W": 0, "D": 0, "L": 0, "Pts": 0}

                    if match_result is None or match_result == "None":
                        continue
                    score_a, score_b = map(int, match_result.split(":"))

                    # Update stats
                    teams_stats[team_a]["P"] += 1
                    teams_stats[team_b]["P"] += 1
                    teams_stats[team_a]["S"][0] += score_a
                    teams_stats[team_a]["S"][1] += score_b
                    teams_stats[team_b]["S"][0] += score_b
                    teams_stats[team_b]["S"][1] += score_a

                    # Win, draw, loss logic
                    if score_a > score_b:
                        teams_stats[team_a]["W"] += 1
                        teams_stats[team_b]["L"] += 1
                        teams_stats[team_a]["Pts"] += 3
                    elif score_a < score_b:
                        teams_stats[team_b]["W"] += 1
                        teams_stats[team_a]["L"] += 1
                        teams_stats[team_b]["Pts"] += 3
                    else:
                        teams_stats[team_a]["D"] += 1
                        teams_stats[team_b]["D"] += 1
                        teams_stats[team_a]["Pts"] += 1
                        teams_stats[team_b]["Pts"] += 1

                # Sort teams by points, then goal difference, then goals scored
                group_results[group] = sorted(
                    teams_stats.items(), key=lambda x: (-x[1]["Pts"], -(x[1]["S"][0] - x[1]["S"][1]), -x[1]["S"][0])
                )

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
        "group_results": group_results,
        "result_dict": result_dict,
    }

    return render(request, "results.html", data)


def info(request):
    teams = Team.objects.all()
    categories = Category.objects.filter(event__is_active=True)
    data = {"teams": teams, "categories": categories}
    return render(request, "info.html", data)


def teamslist(request):
    teams = Team.objects.all()
    data = {"teams": teams}
    return render(request, "teamslist.html", data)


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


@user_passes_test(lambda user: user.is_staff)
def download_detailed(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="ucastnici.csv"'},
    )

    ucastnici = Person.objects.all()
    w = csv.writer(response)
    cols = [i.name.removeprefix("leader.") for i in Person.get_model_fields(Person)]
    w.writerow(cols)
    for obj in ucastnici:
        row = []
        for field in Person.get_model_fields(Person):
            row.append(str(getattr(obj, field.name)))
        w.writerow(row)

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
    if Category.objects.filter(id=id).get().detailed_pdf:
        return HttpResponse(Category.objects.filter(id=id).get().detailed_pdf, content_type="application/pdf")
    messages.error(request, "Detailné výsledky pre túto kategóriu neboli nahrané.")
    return redirect("results", id=id)
