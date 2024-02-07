from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("info", views.info, name="info"),
    path("results", views.results, name="results"),
    path("results/<int:id>/", views.results, name="results"),
    path("download-competitors", views.download_competitors, name="download-competitors"),
    path("download-teams", views.download_teams, name="download-teams"),
]
