from django.utils import timezone

from district.models.assessment import Assessment

# retrieve all the current assessments
import toolbox.utils.exercise as Ex


def get_current_asse(request):
    # get current user
    curr_user = request.user

    # get current assessment
    in_progress = Assessment.objects.filter(
        start_time__lte=timezone.now(),
        end_time__gt=timezone.now(),
        groups__userdc=curr_user)

    return in_progress


# retrieve all the past assessments
def get_past_asse(request):
    # get current user
    curr_user = request.user

    training = Assessment.objects.filter(
        start_time__lt=timezone.now(),
        end_time__lte=timezone.now(),
        training_time__lte=timezone.now(),
        groups__userdc=curr_user)

    return training


# retrieve all the future assessments
def get_future_asse(request):
    # get current user
    curr_user = request.user

    future = Assessment.objects.filter(
        start_time__gt=timezone.now(),
        end_time__gt=timezone.now(),
        groups__userdc=curr_user)

    return future


# give the availability of an assessment (future assessment aren't available)
# param : QuerySet of Assessment
# return a list of dict of {bool is_available, Assessment assessment}
def is_asse_available(assessments):
    list_asse = []
    for asse in assessments:
        list_asse.append({"is_available": asse.start_time.__le__(timezone.now()), "assessment": asse})

    return list_asse


# get exercises of an assessment
# return a dict of {
#   int exit_code,
#   Assessment assessment,
#   dict exercises of {
#       Exercise ex_obj,
#       bool is_triable,
#       list of Language lang_objs}}
def get_asse_exercises(request, id_asse):
    # get current user
    curr_user = request.user
    # get the Assessment object
    curr_asse = Assessment.objects.filter(
        id=id_asse,
        groups__userdc=curr_user
    )

    if len(curr_asse.all()) == 0:
        return {"exit_code": 4}
    result = is_asse_available(curr_asse)[0]
    # only accessible assessments
    if not result["is_available"]:
        return {"exit_code": 3}

    # dictionary for initial data
    context = {
        "exit_code": 0,
        "assessment": curr_asse.first(),
        "exo2tests": Ex.is_exo_triable(curr_user, curr_asse.first(), curr_asse.first().test_id.exo2test_set.all())
    }

    # Use context in the template and render response view
    return context
