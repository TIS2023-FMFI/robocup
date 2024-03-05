import csv
import json
import random
import string
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template
from unidecode import unidecode
from xhtml2pdf import pisa
from itertools import combinations
from web.org.forms import CSVImportForm
from web.users.models import RobocupUser, RobocupUserManager

from ..leader.models import Person, Team
from .forms import (
    BulkCheckInFormSet,
    EventToCopyFromForm,
    ExpeditionLeaderForm,
    JSONUploadForm,
    PDFUploadForm,
    StaffUserCreationForm,
)
from .models import Category, Event


@user_passes_test(lambda user: user.is_staff)
def org_panel(request):
    if request.method == "POST":
        form = ExpeditionLeaderForm(request.POST)
        event_form = EventToCopyFromForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["search_query"]
            results = Person.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))

        else:
            results = Person.objects.filter()
    else:
        form = ExpeditionLeaderForm()
        event_form = EventToCopyFromForm(request.POST)
        results = Person.objects.filter(is_supervisor=True)
    categories = Category.objects.filter(event__is_active=True)
    context = {"form": form, "event_form": event_form, "results": results, "categories": categories}
    return render(request, "org-panel.html", context)


@user_passes_test(lambda user: user.is_staff)
def check_in(request, id):
    user_persons = Person.objects.filter(user_id=id).order_by("last_name")
    user_teams = Team.objects.filter(user_id=id)

    if request.method == "POST":
        formset = BulkCheckInFormSet(request.POST, prefix="person")
        if formset.is_valid():
            for form, person in zip(formset, user_persons):
                person.checked_in = form.cleaned_data["checked_in"]
                person.save()
            messages.success(request, "Check-in ulozeny")
            return redirect("org-panel")
    else:
        formset = BulkCheckInFormSet(
            prefix="person", initial=[{"checked_in": person.checked_in, "name": str(person)} for person in user_persons]
        )
    context = {
        "formset": formset,
        "user_persons": user_persons,
        "user_teams": user_teams,
        "checked_user": id,
    }
    return render(request, "check-in.html", context)


@user_passes_test(lambda user: user.is_staff)
def download_categories(request):
    category = Category.objects.filter(event__is_active=True)
    for cat in category:
        if cat.results is not None:
            cat.results = None
    data = serializers.serialize("json", category)
    response = HttpResponse(
        data,
        content_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="categories.json"'},
    )
    return response


@user_passes_test(lambda user: user.is_staff)
def download_category(request, id):
    category = Category.objects.filter(id=id)
    for cat in category:
        if cat.results is not None:
            cat.results = None
    data = serializers.serialize("json", category)
    response = HttpResponse(
        data,
        content_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="category_{category.get().name}.json"'},
    )
    return response


@user_passes_test(lambda user: user.is_superuser)
def import_json(request):
    if request.method == "POST":
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES["json_file"]
            data = json.load(json_file)

            # Process data and save it to the database
            # This depends on the structure of your JSON and your model
            for item in data:
                obj = Category.create(item)
                if obj is not None:
                    print(item)
                    obj.save()
                else:
                    print(f"{item}: {obj}")
            messages.success(request, "JSON importovaný")
            return redirect("org-panel")

    else:
        form = JSONUploadForm()

    return render(request, "import-json.html", {"form": form})


def import_pdf(request, id):
    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES["pdf_file"]
            category = Category.objects.filter(id=id).get()
            category.detailed_pdf = pdf_file
            category.save()
            messages.success(request, "PDF importované")
            return redirect("org-panel")
    else:
        form = PDFUploadForm()
    return render(request, "import-pdf.html", {"form": form})


@user_passes_test(lambda user: user.is_superuser)
def copy_categories_from_last_event(request):
    if request.method == "POST":
        form = EventToCopyFromForm(request.POST)
        if form.is_valid():
            source_event = form.cleaned_data.get("source_event")
            dest_event = form.cleaned_data.get("destination_event")
            print(source_event, dest_event)
            source_categories = Category.objects.filter(event=source_event)
            for cat in source_categories:
                cat.pk = None
                cat.results = None
                cat.event = dest_event
                cat.save()
    return redirect("org-panel")


def create_staff_user(request):
    if request.method == "POST":
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            # password = User.objects.make_random_password(length=16)
            if not RobocupUser.objects.filter(email=email).exists():
                # Create a new user and set them as staff
                user = RobocupUserManager.create_user(
                    self=RobocupUserManager(), email=email, password=password, is_staff=True
                )
                user.save()
                send_mail(
                    "ucet organizatora robocup.skse.sk",
                    f"Administrátor stránky robocup.skse.sk pre Vás vytvoril\n"
                    f"účet organizátora s nasledujúcimi prihlasovacími údajmi:\n"
                    f"\nprihlasovací e-mail: {email}\nHeslo: {password}\n\n"
                    f"po prihlásení si toto heslo môžete zmeniť na stránke:\n\n"
                    f"    https://robocup.skse.sk/change-password .\n\n"
                    f"Do systému sa prihlásite na stránke https://robocup.skse.sk/\n",
                    from_email="robocup@dai.fmph.uniba.sk",
                    recipient_list=[user.email],
                )
                return redirect("/home")
            else:
                messages.error(request, "Používateľ s touto e-mailovou adresou už existuje.")
    else:
        form = StaffUserCreationForm()

    return render(request, "create_staff_user.html", {"form": form})


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Vaše heslo sa podarilo úspešne zmeniť!")
            return redirect("/home")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change-password.html", {"form": form})


def download_team_for_category(request, id):
    category = Category.objects.filter(id=id)
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="teamy_cat{unidecode(category.get().name)}.csv"'},
    )
    teamy = Team.objects.filter(categories=id)
    w = csv.writer(response)
    w.writerow(["nazov", "poradie", "body"])

    for t in teamy:
        w.writerow([t.team_name, 0, 0])

    return response


def upload_category_results(request, id):
    if request.method == "POST":
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"].read().decode("utf-8").splitlines()
            csv_reader = csv.DictReader(csv_file)
            json_array = []
            all_team_names = Team.objects.values_list("team_name", flat=True)

            for row in csv_reader:
                if row["nazov"] in all_team_names:
                    json_array.append(row)
            instance = get_object_or_404(Category, id=id)
            instance.results = json_array
            instance.save()
            messages.success(request, "Výsledky boli nahrané.")
            return redirect("/org-panel")

    else:
        form = CSVImportForm()
    category = Category.objects.filter(id=id).get()
    return render(request, "upload_category_results.html", {"form": form, "category": category})


def diploms_for_category(request, id):
    category = Category.objects.filter(id=id).get()
    results = dict()
    if not category.results:
        messages.error(request, "Výsledky pre hľadanú kategóriu ešte neboli vyplnené.")
        return redirect("org-panel")

    # Check if it's a soccer category and has a final group
    if category.is_soccer:
        ordered_results = order_group_results(category)
        if "Final Group" not in ordered_results:
            messages.error(request, "Finálna skupina ešte nebola vygenerovaná.")
            return redirect("org-panel")
        # For soccer categories, use only final group results
        print(ordered_results["Final Group"])
        results = {team[0]: pos+1 for pos, team in enumerate(ordered_results["Final Group"])}
        print(results)
    else:
        # For non-soccer categories, the existing logic is kept
        for rec in category.results:
            print(rec["nazov"], ": ", rec["poradie"])
            results[rec["nazov"]] = int(rec["poradie"])

    return make_diplom(category=category, results=results)

@user_passes_test(lambda user: user.is_staff)
def make_diplom(category, results):
    event = Event.objects.filter(is_active=True).get()
    _teams = Team.objects.filter(categories=category)
    print(_teams)
    teams = dict()
    for team in _teams:
        if team.team_name in results:
            teams[team] = results[team.team_name]
    teams = dict(sorted(teams.items(), key=lambda item: item[1]))
    context = {
        "event": event,
        "category": category,
        "teams": teams,
    }
    pdf = html_to_pdf("diplom.html", context_dict=context)

    # rendering the template
    return HttpResponse(pdf, content_type="application/pdf")


def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None


def edit_results_page(request, id):
    category = get_object_or_404(Category, id=id)
    teams = Team.objects.filter(categories=id)

    # Ak nie sú výsledky, vygenerujte kombinácie zápasov a uložte ich do category.results
    if not category.results:
        total_teams = len(teams)
        max_teams = category.max_teams_per_group
        total_groups = (total_teams + max_teams - 1) // max_teams  # Ceiling division to include incomplete group
        if not category.results:
            grouped_matches = {}
            for group_number in range(1, total_groups + 1):
                start_index = (group_number - 1) * max_teams
                end_index = min(start_index + max_teams, total_teams)  # Ensure we don't go out of bounds
                group_teams = teams[start_index:end_index]
                match_combinations = list(combinations([team.team_name for team in group_teams], 2))
                random.shuffle(match_combinations)
                grouped_matches[f'Group {group_number}'] = {
                    f'{match[0]}-{match[1]}': None for match in match_combinations
                }
            category.results = json.dumps(grouped_matches)
            category.save()
    if request.method == 'POST':
        action = request.POST.get('action')
        # Load the current results structure
        grouped_results_dict = json.loads(category.results)

        if action == 'generate_second_round':

            for group, matches in grouped_results_dict.items():
                second_round_matches = {f'{match}-2.kolo': "None" for match in matches}
                grouped_results_dict[group].update(second_round_matches)
        elif action == 'save':
            # Iterate over each item in the POST data
            for key, new_score in request.POST.items():
                # Skip csrf and other non-match keys
                if key.startswith('csrf') or not '-' in key:
                    continue

                # Find the right group and match to update
                for group, matches in grouped_results_dict.items():
                    if key in matches:
                        # Update the match score
                        grouped_results_dict[group][key] = new_score
                        break  # Match found and updated, no need to check other groups
        if action == 'generate_final_group':
            ordered_groups = order_group_results(category)
            final_group_teams = []
            for group, teams in ordered_groups.items():
                top_teams = [team[0] for team in teams[:category.advancing_teams_per_group]]
                final_group_teams.extend(top_teams)
            # Generate final group matches
            final_group_matches = list(combinations(final_group_teams, 2))
            final_group = {f'{match[0]}-{match[1]}-final': 'None' for match in final_group_matches}
            # Add final group to results and save
            grouped_results_dict['Final Group'] = final_group
            category.results = json.dumps(grouped_results_dict)
            category.save()

        # Save the updated results back to the category object
        category.results = json.dumps(grouped_results_dict)
        category.save()
        # Redirect to refresh and prevent form re-submission
        return redirect('edit-results', id=id)
    # Prevod reťazca na slovník pre zobrazenie aktuálnych výsledkov v šablóne
    current_results = json.loads(category.results)
    second_round_generated = any(
        "-2.kolo" in match for group_matches in current_results.values() for match in group_matches)
    final_group_generated = 'Final Group' in current_results
    return render(request, 'edit_results_page.html', {
        "category": category,
        "current_results": current_results,
        "second_round_generated": second_round_generated,
        "final_group_generated": final_group_generated
    })


def order_group_results(category):
    group_results = {}
    result_dict = json.loads(category.results)
    # Assuming result_dict is structured with group keys and match results
    for group, matches in result_dict.items():
        teams_stats = {}
        for match_teams, match_result in matches.items():
            # print(f"match_result: {match_result}")
            team_a, team_b = match_teams.split('-')[0:2]
            # Initialize or update team stats
            for team in [team_a, team_b]:
                if team not in teams_stats:
                    teams_stats[team] = {'P': 0, 'S': [0, 0], 'W': 0, 'D': 0, 'L': 0, 'Pts': 0}
            if match_result == None or match_result == 'None':
                continue
            score_a, score_b = map(int, match_result.split(':'))

            # Update stats
            teams_stats[team_a]['P'] += 1
            teams_stats[team_b]['P'] += 1
            teams_stats[team_a]['S'][0] += score_a
            teams_stats[team_a]['S'][1] += score_b
            teams_stats[team_b]['S'][0] += score_b
            teams_stats[team_b]['S'][1] += score_a

            # Win, draw, loss logic
            if score_a > score_b:
                teams_stats[team_a]['W'] += 1
                teams_stats[team_b]['L'] += 1
                teams_stats[team_a]['Pts'] += 3
            elif score_a < score_b:
                teams_stats[team_b]['W'] += 1
                teams_stats[team_a]['L'] += 1
                teams_stats[team_b]['Pts'] += 3
            else:
                teams_stats[team_a]['D'] += 1
                teams_stats[team_b]['D'] += 1
                teams_stats[team_a]['Pts'] += 1
                teams_stats[team_b]['Pts'] += 1
        # Sort teams by points, then goal difference, then goals scored
        group_results[group] = sorted(teams_stats.items(),
                                      key=lambda x: (-x[1]['Pts'], -(x[1]['S'][0] - x[1]['S'][1]), -x[1]['S'][0]))
    return group_results
