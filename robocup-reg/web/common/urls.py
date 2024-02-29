from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("info", views.info, name="info"),
    path("results", views.results, name="results"),
    path("results/<int:id>/", views.results, name="results"),
    path("results/detailed/<int:id>", views.detailed_results, name="detailed_results"),
    path("download-competitors", views.download_competitors, name="download-competitors"),
    path("download-detailed", views.download_detailed, name="download-detailed"),
    path("download-teams", views.download_teams, name="download-teams"),
]
