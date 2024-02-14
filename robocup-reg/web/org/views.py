import csv
import json
import random
import string
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
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

from web.org.forms import CSVImportForm
from web.users.models import RobocupUser, RobocupUserManager

from ..leader.models import Person, Team
from .forms import BulkCheckInFormSet, EventToCopyFromForm, ExpeditionLeaderForm, JSONUploadForm, StaffUserCreationForm
from .models import Category, Event


@user_passes_test(lambda user: user.is_staff)
def org_panel(request):
    if request.method == "POST":
        form = ExpeditionLeaderForm(request.POST)
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
            messages.success(request, "JSON importovany")
            return redirect("org-panel")

    else:
        form = JSONUploadForm()

    return render(request, "import-json.html", {"form": form})


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
                    "Your Staff Account Has Been Created",
                    f"Your account has been created with the following"
                    f" credentials:\nUsername: {email}\nPassword: {password}\n"
                    f"you can change this password after login at https://robocup.skse.sk/change-password .",
                    from_email="robocup@thefilip.eu",
                    recipient_list=[user.email],
                )
                login(request, user)
                return redirect("/home")
            else:
                messages.error(request, "User with the email address already exists.")
    else:
        form = StaffUserCreationForm()

    return render(request, "create_staff_user.html", {"form": form})


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
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
    w.writerow(["nazov", "poriadie"])

    for t in teamy:
        w.writerow([t.team_name, 0])

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
    for rec in category.results:
        print(rec["nazov"], ": ", rec["poriadie"])
        results[rec["nazov"]] = int(rec["poriadie"])

    return make_diplom(category=category, results=results)


def make_diplom(category, results):
    event = Event.objects.filter(is_active=True).get()
    _teams = Team.objects.filter(categories=category)
    teams = dict()
    for team in _teams:
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
