import csv

from django.shortcuts import render

from .forms import CSVImportForm


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
