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
from django.contrib import admin
from django.urls import path, include

from district.controllers.exercisecontroller import get_exercise, get_verify
from district.views import main_view, test_view
from district.controllers.assessmentcontroller import get_current, get_past, get_future, get_exercises

urlpatterns = [
    # Documentation Generation (before 'admin' URL in order to avoid interceptions)
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    # Administration View
    path('admin/'    , admin.site.urls),

    # The current assessment View
    path('assessment/current', get_current),
    # The future assessment View
    path('assessment/future', get_future),
    # The past assessment View
    path('assessment/past', get_past),

    # The list of exercises of an assessment View
    path('assessment/exercises/<int:id_asse>', get_exercises),

    # The training exercise View
    path('exercise/write', get_exercise),
    # The verifying exercise View
    path('exercise/inspect', get_verify),

    # just for test
    path('test', test_view),

    # Our views
    path(''          , main_view),
]
