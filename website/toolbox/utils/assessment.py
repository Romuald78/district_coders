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
        groups__userdc=curr_user).distinct()

    return in_progress


# retrieve all the past assessments
def get_past_asse(request):
    # get current user
    curr_user = request.user

    training = Assessment.objects.filter(
        start_time__lt=timezone.now(),
        end_time__lte=timezone.now(),
        training_time__lte=timezone.now(),
        groups__userdc=curr_user).distinct()

    return training


# retrieve all the future assessments
def get_future_asse(request):
    # get current user
    curr_user = request.user

    future = Assessment.objects.filter(
        start_time__gt=timezone.now(),
        end_time__gt=timezone.now(),
        groups__userdc=curr_user).distinct()

    return future


# give the availability of an assessment (future assessment aren't available)
# param : QuerySet of Assessment
# return a list of dict of {bool is_available, Assessment assessment}
def is_asse_available(assessments):
    list_asse = []
    for asse in assessments:
        list_asse.append({"is_available": not is_date_future(asse), "assessment": asse})

    return list_asse

# return a dictionary with assessment IDs as keys
# and a list of assessment IDs in collision as value
def detect_assess_overlaps(past, current, future):
    # store all assessments for this user
    all = []
    # useless to check collision with past assessments
    #for assess in past:
    #    all.append((assess["assessment"].start_time, assess["assessment"]))
    #    all.append((assess["assessment"].end_time,   assess["assessment"]))
    for assess in current:
        all.append((assess["assessment"].start_time, assess))
        all.append((assess["assessment"].end_time,   assess))
    for assess in future:
        all.append((assess["assessment"].start_time, assess))
        all.append((assess["assessment"].end_time,   assess))
    # Sort by time
    all = sorted(all, key=lambda x: x[0])
    #
    active = []
    out    = {}
    for a in all:
        assess = a[1]
        if assess in active:
            # this is an end
            active.remove(assess)
        else:
            # this is a start
            active.append(assess)
            assess["overlaps"] = []
            if len(active) > 1:
                for other in active:
                    if assess != other:
                        if other["assessment"] not in assess["overlaps"]:
                            assess["overlaps"].append(other["assessment"])
                        if assess["assessment"] not in other["overlaps"]:
                            other["overlaps"].append(assess["assessment"])

# get exercises of an assessment
# return a dict of {
#   int exit_code,
#   Assessment assessment,
#   dict of exo2test_id->{
#       Exo2Test ex2tst_obj,
#       bool is_triable,
#       list of ExoTest2Lang ex_tst_lng
#       bool is_redirected,
#       int asse_id
#       }
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
    # adding stat for each ex2tst
    exo_triable = Ex.is_exo_triable(curr_user, curr_asse.first(), curr_asse.first().test.exo2test_set.all().order_by("rank"))
    for ex2tst in exo_triable:
        nb_test_try = 0
        nb_test_pass = 0
        nb_train_try = 0
        nb_train_pass = 0
        for extstlng in exo_triable[ex2tst]["ex_tst_lng"]:
            nb_test_try += extstlng.nb_test_try
            nb_test_pass += extstlng.nb_test_pass
            nb_train_try += extstlng.nb_train_try
            nb_train_pass += extstlng.nb_train_pass
        exo_triable[ex2tst]["result_test"] = int(0 if nb_test_try == 0 else 100*nb_test_pass/nb_test_try)
        exo_triable[ex2tst]["result_train"] = int(0 if nb_train_try == 0 else 100*nb_train_pass/nb_train_try)

    context = {
        "exit_code": 0,
        "assessment": curr_asse.first(),
        "exo2tests": exo_triable
    }

    # Use context in the template and render response view
    return context


# param Assessment asse
def is_date_current(asse):
    return asse.start_time.__le__(timezone.now()) and timezone.now().__lt__(asse.end_time)


# param Assessment asse
# recently past assessment, thus no training mode available
def is_date_past_wo_training(asse):
    return asse.start_time.__lt__(timezone.now()) and asse.end_time.__le__(timezone.now()) and timezone.now().__lt__(asse.training_time)


# param Assessment asse
# in training mode
def is_date_trainable(asse):
    return asse.start_time.__lt__(timezone.now()) and asse.end_time.__le__(timezone.now()) and asse.training_time.__le__(timezone.now())


# param Assessment asse
def is_date_future(asse):
    return not asse.start_time.__le__(timezone.now())

