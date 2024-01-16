from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render


@user_passes_test(lambda user: user.is_superuser)
def admin_panel(request):
    return render(request, "admin-panel.html")
