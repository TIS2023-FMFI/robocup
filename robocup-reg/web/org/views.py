import json

from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from ..leader.models import Person
from .forms import BulkCheckInFormSet, ExpeditionLeaderForm, JSONUploadForm
from .models import Category


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


def check_in(request, id):
    people = Person.objects.filter(user=id)

    context = {"people": people, "checked_user": id}
    if request.method == "POST":
        formset = BulkCheckInFormSet(request.POST)
        if formset.is_valid():
            for form, person in zip(formset, people):
                person.checked_in = form.cleaned_data["checked_in"]
                person.save()
    else:
        formset = BulkCheckInFormSet(initial=[{"checked_in": person.checked_in} for person in people])
        print(formset)
    context["form"] = formset

    return render(request, "check-in.html", context)


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
