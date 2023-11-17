from django.urls import path

from . import views

urlpatterns = [
    path("leader-panel", views.leader_panel, name="leader-panel"),
]
