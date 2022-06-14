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
from django.contrib.auth import views as auth_views

from district.controllers.exercisecontroller import ctrl_exercise_write, ctrl_json_exercise_inspect, ctrl_exercise_details
from district.views import main_view, test_view
from district.controllers.assessmentcontroller import ctrl_current_asse, ctrl_past_asse, ctrl_future_asse, ctrl_asse_details
from website import settings
from website.settings import LOGIN_URL

urlpatterns = [
    # Documentation Generation (before 'admin' URL in order to avoid interceptions)
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    # Administration View
    path('admin/'    , admin.site.urls),
    # Authent views
    path("accounts/", include("django.contrib.auth.urls")),
    # current assessments View
    path('assessment/current', ctrl_current_asse),
    # future assessments View
    path('assessment/future', ctrl_future_asse),
    # past assessments View
    path('assessment/past', ctrl_past_asse),

    # The list of exercises of an assessment View
    path('assessment/details/<int:id_asse>', ctrl_asse_details),

    # The wording(without code editor) of an exercise
    path('exercise/details', ctrl_exercise_details),
    # The training exercise View (with code editor)
    path('exercise/write', ctrl_exercise_write),
    # The verifying exercise View
    path('exercise/inspect', ctrl_json_exercise_inspect),

    # just for test
    path('test', test_view),

    # Our views
    path(''          , main_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
