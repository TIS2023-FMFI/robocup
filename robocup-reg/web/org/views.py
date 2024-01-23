import json
import random
import string

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from web.users.models import RobocupUserManager

from ..leader.models import Person
from .forms import BulkCheckInFormSet, EventToCopyFromForm, ExpeditionLeaderForm, JSONUploadForm, StaffUserCreationForm
from .models import Category


@user_passes_test(lambda user: user.is_staff)
def org_panel(request):
    results = {}
    if request.method == "POST":
        form = ExpeditionLeaderForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_query"]
            results = Person.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))

        else:
            results = Person.objects.filter()
    else:
        form = ExpeditionLeaderForm()
        results = Person.objects.filter(is_supervisor=True)
    return render(request, "org-panel.html", {"form": form, "results": results})


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
    category = Category.objects.all()
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

    else:
        form = JSONUploadForm()

    return render(request, "import-json.html", {"form": form})


@user_passes_test(lambda user: user.is_superuser)
def copy_categories_from_last_event(request):
    if request.method == "POST":
        form = EventToCopyFromForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = EventToCopyFromForm()
    return render(request, "org-panel.html", {"form": form})


def create_staff_user(request):
    if request.method == "POST":
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            # password = User.objects.make_random_password(length=16)
            # TODO check if email is free

            # Create a new user and set them as staff
            user = RobocupUserManager.create_user(
                self=RobocupUserManager(), email=email, password=password, is_staff=True
            )
            print(user)
            user.save()

            # Send an email to the user
            send_mail(
                "Your Staff Account Has Been Created",
                f"Your account has been created with the following"
                f" credentials:\nUsername: {email}\nPassword: {password}",
                from_email="robocup@thefilip.eu",
                recipient_list=[user.email],
            )
            login(request, user)
            return redirect("/home")
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
