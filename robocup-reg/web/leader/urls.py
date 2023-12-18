from django.urls import path

from . import views

urlpatterns = [
    path("", views.leader_panel, name="leader_panel"),
    path("leader-panel", views.leader_panel, name="leader_panel"),
    #    path("leader_panel/team_assembly", views.team_assembly, name="team_assembly"),
    #    path("leader_panel/add_supervisor", views.add_supervisor, name="add_supervisor"),
    #    path("leader_panel/add_competitor", views.add_competitor, name="add_competitor"),
]
