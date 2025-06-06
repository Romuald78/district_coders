from django.contrib.admin.sites import site
from django.shortcuts import redirect


def ctrl_admin_login(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return site.index(request)
    return redirect('/')



