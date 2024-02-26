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
    path("org-panel/copy-event/", views.copy_categories_from_last_event, name="copy-event"),
    path("create-staff-user", views.create_staff_user, name="create-staff-user"),
    path("change-password", views.change_password, name="change-password"),
    path(
        "org-panel/download-teams-for-category/<int:id>/",
        views.download_team_for_category,
        name="download-teams-for-category",
    ),
    path("org-panel/upload-category-results/<int:id>/", views.upload_category_results, name="upload-category-results"),
    path("org-panel/diplom/<int:id>", views.diploms_for_category, name="diplom"),
    # path("org-panel/competitor/edit/<int:id>/", leader_views.competitor_edit, name="competitor_edit_2"),
]
