from datetime import timedelta

from django.db.models import Q, F
from django.utils import timezone

from district.models.assessment import Assessment
from district.models.exercise import Exercise
from district.models.exo2test import Exo2Test

import toolbox.utils.assessment as Asse


# check if a Set of Exercise are triable or not (only read access)
# param :
#   User curr_user
#   Assessment curr_asse
#   QuerySet of Exo2Test all_exo2test
# return :
#   dict of exo2test_id->{
#       Exo2Test ex2tst_obj,
#       bool is_triable,
#       list of ExoTest2Lang ex_tst_lng
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

    all_other_asse = Assessment.objects.filter(
        ~Q(id=curr_asse.id),
        groups__userdc=curr_user
    )

    # getting the higher rank of the solved exercises
    ranking_max_all_exo2test = Exo2Test.objects.filter(
        test__assessment=curr_asse,
        solve_percentage_req__lte=F("exotest2lang__testresult__solve_percentage")
    ).order_by("-rank")
    # if no exercises have been completed yet
    if len(ranking_max_all_exo2test.all()) == 0:
        # the user start the assessment
        # getting the lower rank exercise
        min_unsolved_rank = Exo2Test.objects.filter(test__assessment=curr_asse).order_by("rank").first().rank
    else:
        max_solved_rank = ranking_max_all_exo2test.first().rank
        # getting the lower rank greater than max_solved_rank
        ranking_min_all_exo2test = Exo2Test.objects.filter(
            test__assessment=curr_asse,
            rank__gt=max_solved_rank
        ).order_by("rank")
        # if no exercises have been tested yet
        if len(ranking_min_all_exo2test.all()) == 0:
            # the user end the assessment
            # letting the user access to nonexistent exercise (rank too high)
            min_unsolved_rank = max_solved_rank + 1
        else:
            min_unsolved_rank = ranking_min_all_exo2test.first().rank


    exos = {}
    for ex2test in all_exo2test:
        # getting languages available
        all_ex_tst_lng = []
        for ex_tst_lng in ex2test.exotest2lang_set.all():
            # lang = ex_tst_lng.lang_id
            all_ex_tst_lng.append(ex_tst_lng)
        # set is_triable to False the exercise of a rank already passed
        exos[ex2test.id] = {
            "ex2tst_obj": ex2test,
            "is_triable": True,
            "ex_tst_lng": all_ex_tst_lng,
            "is_redirected": False,
            "asse_id": curr_asse.id
        }
        if ex2test.rank >= min_unsolved_rank:
            exos[ex2test.id]["is_triable"] = ex2test.rank == min_unsolved_rank
        else:
            is_exo_solved = False
            for etl in all_ex_tst_lng:
                if len(etl.testresult_set.all()) != 0 and etl.testresult_set.first().solve_percentage >= etl.exo2test.solve_percentage_req:
                    is_exo_solved = True
            exos[ex2test.id]["is_triable"] = not is_exo_solved

    # now, we set elements from exos
    for asse in all_other_asse:
        for ex2test in asse.test.exo2test_set.all():
            if ex2test.id in exos:
                # if assessment is in process
                if Asse.is_date_current(curr_asse):
                    pass
                else: # if assessment is not in process
                    # if assessment is past but not in training mode
                    if Asse.is_date_past_wo_training(curr_asse):
                        # if the assessment is in process
                        if Asse.is_date_current(asse):
                            exos[ex2test.id]["asse_id"] = asse.id
                            exos[ex2test.id]["is_redirected"] = True
                        elif not exos[ex2test.id]["is_redirected"]:
                            exos[ex2test.id]["is_triable"] = False
                    else:
                        # if the assessment is in process
                        if Asse.is_date_current(asse):
                            exos[ex2test.id]["asse_id"] = asse.id
                            exos[ex2test.id]["is_redirected"] = True
                        # if not redirected (to in process asse) and if assessment is past but not in training mode
                        elif not exos[ex2test.id]["is_redirected"] and Asse.is_date_past_wo_training(curr_asse):
                            exos[ex2test.id]["is_triable"] = False
                            exos[ex2test.id]["asse_id"] = asse.id
                            exos[ex2test.id]["is_redirected"] = True
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
        exo2test__test__assessment=asse_id,
        exo2test__test__assessment__groups__userdc=curr_user)
    if ex_id == 0 or asse_id ==0 or len(ex_obj) == 0:
        return {"exit_code": 4}

    return {"exit_code": 0, "ex_obj": ex_obj}


# return a dict containing the wording of an exercise
# dict of {
#   int exit_code:
#       3 : Access denied
#       [ exit code of exercise.get_exercise ]
#   Exo2Test ex2tst_obj
#   bool is_triable
#   List of ExoTest2Lang ex_tst_lng}
def get_exercise_details(curr_user, ex2test_id, asse_id):
    # check if the assessment is reachable in this assessment
    ex_id = Exercise.objects.filter(exo2test=ex2test_id).first().id
    result = get_exercise(curr_user, ex_id, asse_id)
    if result["exit_code"] != 0:
        return result

    curr_asse = Assessment.objects.filter(id=asse_id, groups__userdc=curr_user)
    if len(curr_asse.all()) == 0:
        return {"exit_code": 4}

    if not Asse.is_asse_available(curr_asse)[0]["is_available"]:
        return {"exit_code": 3}

    all_exo2test = Exo2Test.objects.filter(id=ex2test_id, test__assessment__groups__userdc=curr_user)
    if len(all_exo2test.all()) == 0:
        return {"exit_code": 4}

    exos = is_exo_triable(curr_user, curr_asse.first(), all_exo2test)
    return {"exit_code": 0,
            "ex2tst_obj": exos[ex2test_id]["ex2tst_obj"],
            "is_triable": exos[ex2test_id]["is_triable"],
            "ex_tst_lng": exos[ex2test_id]["ex_tst_lng"]}


# return a dict containing the wording of an exercise
# dict of {
#   int exit_code:
#       3 : Access denied
#       [ exit code of exercise.get_exercise ]
#   Exo2Test ex2tst_obj
#   List of ExoTest2Lang ex_tst_lng}
def get_exercise_write(curr_user, ex2test_id, asse_id):
    # check if the assessment is reachable in this assessment
    ex_id = Exercise.objects.filter(exo2test=ex2test_id).first().id
    result = get_exercise(curr_user, ex_id, asse_id)
    if result["exit_code"] != 0:
        return result

    curr_asse = Assessment.objects.filter(id=asse_id, groups__userdc=curr_user)
    if len(curr_asse.all()) == 0:
        return {"exit_code": 4}

    if not Asse.is_asse_available(curr_asse)[0]["is_available"]:
        return {"exit_code": 3}

    all_exo2test = Exo2Test.objects.filter(id=ex2test_id, test__assessment__groups__userdc=curr_user)
    if len(all_exo2test.all()) == 0:
        return {"exit_code": 4}

    exos = is_exo_triable(curr_user, curr_asse.first(), all_exo2test)
    if exos[ex2test_id]["is_triable"]:
        return {"exit_code": 0, "ex2tst_obj": exos[ex2test_id]["ex2tst_obj"], "ex_tst_lng": exos[ex2test_id]["ex_tst_lng"]}
    else:
        return {"exit_code": 3}
