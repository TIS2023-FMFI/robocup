from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("results", views.results, name="results"),
    path("download-competitors", views.download_competitors, name="download-competitors"),
    path("download-teams", views.download_teams, name="download-teams"),
    path("download-teams-for-category/<int:id>/", views.download_team_for_category, name="download-teams-for-category"),
]
