from django.urls import path

from . import views

urlpatterns = [
    path("org-panel", views.org_panel, name="org-panel"),
    path("check_in", views.check_in, name="check_in"),
    path("categories", views.categories, name="categories"),
]
