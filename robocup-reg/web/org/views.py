import csv

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from .forms import CSVImportForm
from .models import Category


def org_panel(request):
    return render(request, "org-panel.html")


def import_csv(request):
    if request.method == "POST":
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"].read().decode("utf-8").splitlines()
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                print(row)

    else:
        form = CSVImportForm()

    return render(request, "results.html", {"form": form})


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
