import json

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from ..leader.models import Person
from .forms import BulkCheckInFormSet, EventToCopyFromForm, ExpeditionLeaderForm, JSONUploadForm
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
