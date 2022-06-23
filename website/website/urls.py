"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from district.controllers.ctrl_exercise import ctrl_exercise_write, ctrl_json_exercise_inspect, ctrl_exercise_details
from district.controllers.ctrl_testresult import ctrl_json_testresult_exists
from district.controllers.ctrl_user import ctrl_user_profile, ctrl_user_signup
from toolbox.utils.user import ctrl_user_register
from district.controllers.ctrl_main import ctrl_home
from district.controllers.ctrl_assessment import ctrl_asse_details
from toolbox.utils.assessment import get_current_asse, get_past_asse, get_future_asse
from website import settings

urlpatterns = [
    # Documentation Generation (before 'admin' URL in order to avoid interceptions)
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    # Administration View
    path('admin/'    , admin.site.urls),

    # Authent views
    path("accounts/", include("django.contrib.auth.urls")),
    # Let a user join a group
    path('accounts/signup/', ctrl_user_signup),
    # The user profile View
    path('accounts/profile/', ctrl_user_profile),
    # Let a user join a group
    path('accounts/register/', ctrl_user_register),

    # The list of exercises of an assessment View
    path('assessment/details/<int:id_asse>', ctrl_asse_details),

    # The wording(without code editor) of an exercise
    path('exercise/details/', ctrl_exercise_details),
    # The training exercise View (with code editor)
    path('exercise/write/', ctrl_exercise_write),
    # Verify an exercise
    path('exercise/inspect/', ctrl_json_exercise_inspect),
    # Verify the existence of a TestResult
    path('exercise/createstat/', ctrl_json_testresult_exists),

    # HOME
    path('', ctrl_home),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
