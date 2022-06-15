from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone

from district.models.assessment import Assessment
from district.models.exotest2lang import ExoTest2Lang
from district.models.group import GroupDC

from website.settings import LOGIN_URL


# display all the current assessments
@login_required(login_url=LOGIN_URL)
def ctrl_current_asse(request):
    # get current user
    curr_user = request.user

    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get current assessment
    context["assessments"] = Assessment.objects.filter(
        start_time__lte=timezone.now(),
        end_time__gt=timezone.now(),
        groups__userdc=curr_user)

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


# display all the past assessments
@login_required(login_url=LOGIN_URL)
def ctrl_past_asse(request):
    # get current user
    curr_user = request.user

    # get current user
    curr_user = request.user

    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get past assessment
    context["assessments"] = Assessment.objects.filter(
        start_time__lt=timezone.now(),
        end_time__lte=timezone.now(),
        training_time__lte=timezone.now(),
        groups__userdc=curr_user)

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


# display all the future assessments
@login_required(login_url=LOGIN_URL)
def ctrl_future_asse(request):
    # get current user
    curr_user = request.user

    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/assessment.html')

    # get future assessment
    context["assessments"] = Assessment.objects.filter(
        start_time__gt=timezone.now(),
        end_time__gt=timezone.now(),
        groups__userdc=curr_user)

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


# display the list of exercises in an assessment
@login_required(login_url=LOGIN_URL)
def ctrl_asse_details(request, id_asse):
    # get current user
    curr_user = request.user
    # get the Assessment object
    curr_asse = Assessment.objects.filter(
        id=id_asse,
        start_time__lt=timezone.now(),
        groups__userdc=curr_user
    )
    # only accessible assessments
    if not curr_asse.exists():
        return HttpResponse("Access denied")

    # dictionary for initial data
    context = {"assessment": curr_asse}

    # Load view template
    template = loader.get_template('district/exercisesAssess.html')

    # TEST
    all_other_asse = Assessment.objects.filter(
        ~Q(id=id_asse),
        groups__userdc=curr_user
    )

    # let's build a dictionary  composed by all exercises of the assessment
    exos = {}
    for ex2test in curr_asse.first().test_id.exo2test_set.all():
        ex = ex2test.exercise_id
        exos[ex.id] = {"ex_obj": ex, "is_available": True, "lang_objs": []}
        # adding languages available
        for ex_tst_lng in ex2test.exotest2lang_set.all():
            lang = ex_tst_lng.lang_id
            exos[ex.id]["lang_objs"].append(lang)

    # now, we set or remove elements from exos
    for asse in all_other_asse:
        for ex2test in asse.test_id.exo2test_set.all():
            ex = ex2test.exercise_id
            if ex.id in exos:
                # if the assessment is in progress
                if asse.start_time.__le__(timezone.now()) and timezone.now().__lt__(asse.end_time):
                    exos[ex.id]["is_available"] = False
                elif asse.start_time.__gt__(timezone.now()):  # if the assessment will start in the future
                    del exos[ex.id]

    context["exercises"] = exos
    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))