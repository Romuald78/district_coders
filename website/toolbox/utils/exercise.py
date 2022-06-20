from django.db.models import Q
from django.utils import timezone

from district.models.assessment import Assessment
from district.models.exercise import Exercise
from district.models.exo2test import Exo2Test

import toolbox.utils.assessment as Asse


# check if a Set of Exercise are triable or not (only read access)
# param :
#   User curr_user
#   Assessment curr_asse
#   QuerySet of Exercise exercises
# return :
#   dict exercises of ex_id->{
#       Exercise ex_obj,
#       bool is_triable,
#       list of Language lang_objs,
#       bool is_redirected,
#       int asse_id
#       }
def is_exo_triable(curr_user, curr_asse, all_exo2test):
    # on regarde notre assessment
    # - en cours :
    #     trainable True
    # - P\T :
    #     soit y a un autre en cours
    #         -> on leak le premier lien ex_id, asse_id
    #         -> le champ is_redirected = True
    #         -> trainable True
    #     sinon, c'est
    #         -> trainable False
    # -P :
    #     si y un en cours
    #         -> leak
    #         -> trainable True
    #     s'il y a un P\T
    #         -> trainable False
    #         -> leak
    exos = {}

    for ex2test in all_exo2test:
        ex = ex2test.exercise_id
        exos[ex.id] = {"ex_obj": ex, "is_triable": True, "lang_objs": [], "is_redirected": False, "asse_id": curr_asse.id}
        # adding languages available
        for ex_tst_lng in ex2test.exotest2lang_set.all():
            lang = ex_tst_lng.lang_id
            exos[ex.id]["lang_objs"].append(lang)

    # if assessment is not in process
    if not (curr_asse.start_time.__le__(timezone.now()) and timezone.now().__lt__(curr_asse.end_time)):
        all_other_asse = Assessment.objects.filter(
            ~Q(id=curr_asse.id),
            groups__userdc=curr_user
        )

        # if assessment is past but not in training mode
        if curr_asse.start_time.__lt__(timezone.now()) and curr_asse.end_time.__lt__(timezone.now()) and timezone.now().__lt__(curr_asse.training_time):
            # now, we set elements from exos
            for asse in all_other_asse:
                for ex2test in asse.test_id.exo2test_set.all():
                    ex = ex2test.exercise_id
                    if ex.id in exos:
                        # if the assessment is in process
                        if asse.start_time.__le__(timezone.now()) and timezone.now().__lt__(asse.end_time):
                            exos[ex.id]["asse_id"] = asse.id
                            exos[ex.id]["is_redirected"] = True
                        elif not exos[ex.id]["is_redirected"]:
                            exos[ex.id]["is_triable"] = False
        else:
            # now, we set elements from exos
            for asse in all_other_asse:
                for ex2test in asse.test_id.exo2test_set.all():
                    ex = ex2test.exercise_id
                    if ex.id in exos:
                        # if the assessment is in progress
                        if asse.start_time.__le__(timezone.now()) and timezone.now().__lt__(asse.end_time):
                            exos[ex.id]["asse_id"] = asse.id
                            exos[ex.id]["is_redirected"] = True
                        # if not redirected (to in process asse) and if assessment is past but not in training mode
                        elif not exos[ex.id]["is_redirected"] and curr_asse.start_time.__lt__(timezone.now()) and curr_asse.end_time.__lt__(timezone.now()) and timezone.now().__lt__(curr_asse.training_time):
                            exos[ex.id]["is_triable"] = False
                            exos[ex.id]["asse_id"] = asse.id
                            exos[ex.id]["is_redirected"] = True

    return exos


# check if an Exercise is reachable for a user (in a certain assessment)
# return a dict containing the wording of an exercise
# dict of {
#   int exit_code:
#       4 : exercise not found
#       3 : Access denied
#   Exercise ex_obj}
def get_exercise(curr_user, ex_id, asse_id):
    ex_obj = Exercise.objects.filter(
        id=ex_id,
        exo2test__test_id__assessment=asse_id,
        exo2test__test_id__assessment__groups__userdc=curr_user)
    if ex_id == 0 or asse_id ==0 or len(ex_obj) == 0:
        return {"exit_code": 4}

    return {"exit_code": 0, "ex_obj": ex_obj}


# return a dict containing the wording of an exercise
# dict of {
#   int exit_code:
#       3 : Access denied
#       [ exit code of exercise.get_exercise ]
#   Exercise ex_obj}
def get_exercise_details(curr_user, ex2test_id, asse_id):
    # check if the assessment is reachable in this assessment
    ex_id = Exercise.objects.filter(exo2test=ex2test_id).first().id
    result = get_exercise(curr_user, ex_id, asse_id)
    if result["exit_code"] != 0:
        return result

    curr_asse = Assessment.objects.filter(id=asse_id, groups__userdc=curr_user)

    if not Asse.is_asse_available(curr_asse)[0]["is_available"]:
        return {"exit_code": 3}

    all_exo2test = Exo2Test.objects.filter(id=ex2test_id, test_id__assessment__groups__userdc=curr_user)

    exos = is_exo_triable(curr_user, curr_asse.first(), all_exo2test)
    return {"exit_code": 0, "ex_obj": exos[ex_id]["ex_obj"]}


# return a dict containing the wording of an exercise
# dict of {
#   int exit_code:
#       3 : Access denied
#       [ exit code of exercise.get_exercise ]
#   Exercise ex_obj}
def get_exercise_write(curr_user, ex2test_id, asse_id):
    # check if the assessment is reachable in this assessment
    ex_id = Exercise.objects.filter(exo2test=ex2test_id).first().id
    result = get_exercise(curr_user, ex_id, asse_id)
    if result["exit_code"] != 0:
        return result

    curr_asse = Assessment.objects.filter(id=asse_id, groups__userdc=curr_user)

    if not Asse.is_asse_available(curr_asse)[0]["is_available"]:
        return {"exit_code": 3}

    all_exo2test = Exo2Test.objects.filter(id=ex2test_id, test_id__assessment__groups__userdc=curr_user)

    exos = is_exo_triable(curr_user, curr_asse.first(), all_exo2test)
    if exos[ex_id]["is_triable"]:
        return {"exit_code": 0, "ex_obj": exos[ex_id]["ex_obj"]}
    else:
        return {"exit_code": 3}
