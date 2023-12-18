from django.urls import path

from . import views

urlpatterns = [
    path("org-panel", views.org_panel, name="org-panel"),
    path("import-csv", views.import_csv, name="import"),
]
