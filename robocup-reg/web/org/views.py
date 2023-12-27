import csv

from django.shortcuts import render

from .forms import CSVImportForm
from .models import Record


def org_panel(request):
    return render(request, "org-panel.html")


def import_csv(request):
    if request.method == "POST":
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"].read().decode("utf-8").splitlines()
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                Record.objects.create(team_name=row["Meno tímu"], order=row["Poradie"])

            # return redirect('success_page')  # Redirect to a success page
    else:
        form = CSVImportForm()

    return render(request, "import.html", {"form": form})
