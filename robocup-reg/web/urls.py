"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web.common.urls")),
    path("", include("web.users.urls")),
    path("", include("web.leader.urls")),
    path("", include("web.org.urls")),
    path("", include("web.administrator.urls")),
    path("password_reset/", views.PasswordResetView.as_view(template_name='password_reset_form.html',
            html_email_template_name="email_reset_template.html",
            email_template_name='password_reset_email.html', 
            subject_template_name="password_reset_subject.txt"), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name="password_reset_complete",
    ),
]
