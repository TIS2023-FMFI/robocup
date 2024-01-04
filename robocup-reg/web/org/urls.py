from django.urls import path

from . import views

urlpatterns = [
    path("org-panel", views.org_panel, name="org-panel"),
    path("common/results", views.import_csv, name="import_csv"),
]
