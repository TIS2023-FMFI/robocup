from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from ..leader.models import Person
from .forms import ExpeditionLeaderForm
from .models import Category


def org_panel(request):
    if request.method == "POST":
        form = ExpeditionLeaderForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_query"]
            results = Person.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query), is_supervisor=True
            )

        else:
            results = Person.objects.filter(is_supervisor=True)
    else:
        form = ExpeditionLeaderForm()
        results = Person.objects.filter(is_supervisor=True)
    print(results)
    return render(request, "org-panel.html", {"form": form, "results": results})


def check_in(request, id):
    people = Person.objects.filter(user=id)

    context = {"people": people}
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
