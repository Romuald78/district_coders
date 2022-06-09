from django.http import HttpResponse
from django.template import loader


# Create your views here.
from django.utils import timezone

from district.models import assessment
from district.models.assessment import Assessment

# get all the current assessments
from district.models.exercise import Exercise


def get_current(request):
    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get current assessment
    context["assessments"] = Assessment.objects.filter(start_time__lte=timezone.now(), end_time__gt=timezone.now())

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


# get all the past assessments
def get_past(request):
    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get past assessment
    context["assessments"] = Assessment.objects.filter(end_time__lte=timezone.now())

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


# get the future assessments
def get_future(request):
    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get future assessment
    context["assessments"] = Assessment.objects.filter(start_time__gt=timezone.now())

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


# get the list of exercises in the assessment
def get_exercises(request, id_asse):
    # only trainable exercises
    if Assessment.objects.filter(id=id_asse, training_time__gt=timezone.now()).exists():
        return HttpResponse("Access denied")

    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/exercisesAssess.html')

    # get future assessment
    context["exercises"] = Exercise.objects.filter(exo2test__test_id__assessment=id_asse)

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))
