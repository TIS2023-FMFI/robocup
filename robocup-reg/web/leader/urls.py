from django.urls import path

from . import views

urlpatterns = [
    path("", views.leader_panel, name="leader_panel"),
    path("leader-panel", views.leader_panel, name="leader_panel"),
    path("leader-panel/supervisor/add", views.supervisor_add, name="supervisor_add"),
    path("leader-panel/supervisor/add/<int:id>", views.supervisor_add, name="supervisor_add"),
    path("leader-panel/supervisor/edit/<int:id>/", views.supervisor_edit, name="supervisor_edit"),
    path("leader-panel/supervisor/delete/<int:id>/", views.supervisor_delete, name="supervisor_delete"),
    path("leader-panel/competitor/add", views.competitor_add, name="competitor_add"),
    path("leader-panel/competitor/add/<int:id>/", views.competitor_add, name="competitor_add"),
    path("leader-panel/competitor/edit/<int:id>/", views.competitor_edit, name="competitor_edit"),
    path("leader-panel/competitor/delete/<int:id>/", views.competitor_delete, name="competitor_delete"),
    path("leader-panel/team/add", views.team_add, name="team_add"),
    path("leader-panel/team/add/<int:id>", views.team_add, name="team_add"),
    path("leader-panel/team/edit/<int:id>/", views.team_edit, name="team_edit"),
    path("leader-panel/team/delete/<int:id>/", views.team_delete, name="team_delete"),
    path("leader-panel/team/edit/<int:id>-<int:uid>/", views.team_edit_org, name="team_edit_org"),
]
