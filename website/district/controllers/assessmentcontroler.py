from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from django.db import models


# getCurrent, getPast, getFuture

# Create your views here.
from district.models import assessment
from district.models.assessment import Assessment


def getCurrent(request):
    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get current assessement
    context["result_query"] = Assessment.objects.filter(start_time__lte=datetime.now(), end_time__gte=datetime.now())

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))

def getPast(request):
    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get past assessement
    context["result_query"] = Assessment.objects.filter(end_time__lt=datetime.now())

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))

def getFuture(request):
    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get future assessement
    context["result_query"] = Assessment.objects.filter(start_time__gt=datetime.now())

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))