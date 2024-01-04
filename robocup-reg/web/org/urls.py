from django.urls import path

from ..leader import views as leader_views
from . import views

urlpatterns = [
    path("org-panel", views.org_panel, name="org-panel"),
    #    path("common/results", views.import_csv, name="import_csv"),
    path("download-categories", views.download_categories, name="download-categories"),
    path("download-category/<int:id>/", views.download_category, name="download-category"),
    path("org-panel/check-in/<int:id>/", views.check_in, name="check-in"),
    path("import-json", views.import_json, name="import-json"),
    # path("common/results", views.import_csv, name="import_csv"),
    path("download-categories", views.download_categories, name="download-categories"),
    path("download-category/<int:id>/", views.download_category, name="download-category"),
    path("org-panel/check-in/<int:id>/", views.check_in, name="check-in"),
    path("org-panel/competitor/add/<int:id>", leader_views.competitor_add, name="competitor_add_2"),
]
