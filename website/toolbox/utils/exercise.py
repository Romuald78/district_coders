from django.db.models import Q, F

from district.models.assessment import Assessment
from district.models.exercise import Exercise
from district.models.exo2test import Exo2Test

import toolbox.utils.assessment as Asse

from config.constants import error_message_cnf


# check if a Set of Exercise are triable or not (only read access)
# param :
#   User curr_user
#   Assessment curr_asse
#   QuerySet of Exo2Test all_exo2test
# return :
#   dict of exo2test_id->{
#       Exo2Test ex2tst_obj,
#       bool is_triable,
#       (List of String not_triable_msg),
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
    #         -> on link le premier lien ex_id, asse_id
    #         -> le champ is_redirected = True
    #         -> trainable True
    #     sinon, c'est
    #         -> trainable False
    # -P :
    #     si y un en cours
    #         -> link
    #         -> trainable False
    #     s'il y a un P\T
    #         -> trainable False
    #         -> link

    all_other_asse = Assessment.objects.filter(
        ~Q(id=curr_asse.id),
        groups__userdc=curr_user
    )

    exos = {}
    can_go_ahead = True
    for ex2test in Exo2Test.objects.filter(test__assessment=curr_asse).order_by("rank"):
        if ex2test in all_exo2test:
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
        if Asse.is_date_current(curr_asse):
            if can_go_ahead:
                exotest2lang_set = ex2test.exotest2lang_set.order_by("-testresult__solve_percentage")
                # is_accessible = len(exotest2lang_set.all()) > 0 and (
                #         ex2test.solve_percentage_req == 0 or (
                #             len(exotest2lang_set.first().testresult_set.all()) > 0 and
                #              exotest2lang_set.first().testresult_set.first().solve_percentage >= ex2test.solve_percentage_req
                #         )
                # )
                is_accessible = ex2test.solve_percentage_req == 0 or (
                        len(exotest2lang_set.all()) > 0 and
                        len(exotest2lang_set.first().testresult_set.all()) > 0 and
                        exotest2lang_set.first().testresult_set.first().solve_percentage >= ex2test.solve_percentage_req
                )
                if not is_accessible:
                    can_go_ahead = False
            else:
                if ex2test in all_exo2test:
                    exos[ex2test.id]["is_triable"] = False
                    exos[ex2test.id]["not_triable_msg"] = error_message_cnf.RANK_PERMISSION_TOO_HIGH

    # now, we set elements from exos
    for asse in all_other_asse:
        for ex2test in asse.test.exo2test_set.all():
            if ex2test.id in exos:  # TODO useless condition ?
                # if assessment is not in process
                if not Asse.is_date_current(curr_asse):
                    # if assessment is past but not in training mode
                    if Asse.is_date_past_wo_training(curr_asse):
                        # if the assessment is in process
                        if Asse.is_date_current(asse):
                            exos[ex2test.id]["asse_id"] = asse.id
                            exos[ex2test.id]["is_redirected"] = True
                        elif not exos[ex2test.id]["is_redirected"]:
                            exos[ex2test.id]["is_triable"] = False
                            exos[ex2test.id]["not_triable_msg"] = error_message_cnf.DATE_PERMISSION_PAST_NOT_TRAINING
                    else:
                        # if the assessment is in process
                        if Asse.is_date_current(asse):
                            exos[ex2test.id]["asse_id"] = asse.id
                            exos[ex2test.id]["is_redirected"] = True
                            exos[ex2test.id]["is_triable"] = False
                            exos[ex2test.id]["not_triable_msg"] = error_message_cnf.DATE_PERMISSION_IN_PROCESS
                        # if not redirected (to in process asse) and if assessment is past but not in training mode
                        elif not exos[ex2test.id]["is_redirected"] and Asse.is_date_past_wo_training(curr_asse):
                            exos[ex2test.id]["is_triable"] = False
                            exos[ex2test.id]["not_triable_msg"] = error_message_cnf.DATE_PERMISSION_PAST_NOT_TRAINING
                            exos[ex2test.id]["asse_id"] = asse.id
                            exos[ex2test.id]["is_redirected"] = True
    return exos


# check if an Exercise is reachable for a user (in a certain assessment)
# return a dict containing the wording of an exercise
# dict of {
#   int exit_code:
#       4 : exercise not found
#       3 : Access denied
#   (List of String err_msg)
#   Exercise ex_obj}
def get_exercise(curr_user, ex_id, asse_id):
    ex_obj = Exercise.objects.filter(
        id=ex_id,
        exo2test__test__assessment=asse_id,
        exo2test__test__assessment__groups__userdc=curr_user)
    if ex_id == 0 or asse_id == 0:
        return {"exit_code": 3, "err_msg": error_message_cnf.EXERCISE_NOT_FOUND}
    elif len(ex_obj) == 0:
        return {"exit_code": 4, "err_msg": error_message_cnf.GROUP_PERMISSION_EXERCISE}

    return {"exit_code": 0, "ex_obj": ex_obj}


# return a dict containing the wording of an exercise
# dict of {
#   int exit_code:
#       3 : Access denied
#       [ exit code of exercise.get_exercise ]
#   (List of String err_msg)
#   Exo2Test ex2tst_obj
#   bool is_triable
#   (List of String not_triable_msg)
#   List of ExoTest2Lang ex_tst_lng}
def get_exercise_details(curr_user, ex2test_id, asse_id):
    # check if the assessment is reachable in this assessment
    exercise = Exercise.objects.filter(exo2test=ex2test_id)
    if len(exercise.all()) == 0:
        return {"exit_code": 4, "err_msg": error_message_cnf.EXERCISE_NOT_FOUND}
    ex_id = exercise.first().id
    result = get_exercise(curr_user, ex_id, asse_id)
    if result["exit_code"] != 0:
        return result

    curr_asse = Assessment.objects.filter(id=asse_id, groups__userdc=curr_user, test__exo2test=ex2test_id)
    if len(curr_asse.all()) == 0:
        return {"exit_code": 3, "err_msg": error_message_cnf.GROUP_PERMISSION_ASSESSMENT}

    asse_avail = Asse.is_asse_available(curr_asse)[0]
    if not asse_avail["is_available"]:
        return {"exit_code": 3, "err_msg": asse_avail["not_available_msg"]}

    all_exo2test = Exo2Test.objects.filter(id=ex2test_id, test__assessment__groups__userdc=curr_user)
    if len(all_exo2test.all()) == 0:
        return {"exit_code": 4, "err_msg": error_message_cnf.EXERCISE_NOT_FOUND}

    exos = is_exo_triable(curr_user, curr_asse.first(), all_exo2test)
    rtn_obj = {
        "exit_code": 0,
        "ex2tst_obj": exos[ex2test_id]["ex2tst_obj"],
        "is_triable": exos[ex2test_id]["is_triable"],
        "ex_tst_lng": exos[ex2test_id]["ex_tst_lng"]}
    if not rtn_obj["is_triable"]:
        rtn_obj["not_triable_msg"] = exos[ex2test_id]["not_triable_msg"]
    return rtn_obj


# return a dict containing the wording of an exercise
# dict of {
#   int exit_code:
#       3 : Access denied
#       [ exit code of exercise.get_exercise ]
#   (List of String err_msg)
#   Exo2Test ex2tst_obj
#   List of ExoTest2Lang ex_tst_lng}
def get_exercise_write(curr_user, ex2test_id, asse_id):
    # check if the assessment is reachable in this assessment
    exercise = Exercise.objects.filter(exo2test=ex2test_id)
    if len(exercise.all()) == 0:
        return {"exit_code": 4, "err_msg": error_message_cnf.EXERCISE_NOT_FOUND}
    ex_id = exercise.first().id
    result = get_exercise(curr_user, ex_id, asse_id)
    if result["exit_code"] != 0:
        return result

    curr_asse = Assessment.objects.filter(id=asse_id, groups__userdc=curr_user, test__exo2test=ex2test_id)
    if len(curr_asse.all()) == 0:
        return {"exit_code": 3, "err_msg": error_message_cnf.GROUP_PERMISSION_ASSESSMENT}

    asse_avail = Asse.is_asse_available(curr_asse)[0]
    if not asse_avail["is_available"]:
        return {"exit_code": 3, "err_msg": asse_avail["not_available_msg"]}

    all_exo2test = Exo2Test.objects.filter(id=ex2test_id, test__assessment__groups__userdc=curr_user)
    if len(all_exo2test.all()) == 0:
        return {"exit_code": 4, "err_msg": error_message_cnf.EXERCISE_NOT_FOUND}

    exos = is_exo_triable(curr_user, curr_asse.first(), all_exo2test)
    if exos[ex2test_id]["is_triable"]:
        return {"exit_code": 0, "ex2tst_obj": exos[ex2test_id]["ex2tst_obj"], "ex_tst_lng": exos[ex2test_id]["ex_tst_lng"]}
    else:
        return {"exit_code": 3, "err_msg": exos[ex2test_id]["not_triable_msg"]}


# return an ANSI title
def get_title_console():
    bw_title = "[DISTRICT CODERS]"
    col_title = ""
    red, green, blue = 0, 0, 255

    for letter in bw_title:
        if letter != ' ':
            col_title += f"\33[38;2;{red};{green};{blue}m"
            red += 16
            green += 16
            blue -= 16
            if red > 255:
                red = 255
            if green > 255:
                green = 255
            if blue < 0:
                blue = 0
        col_title += letter
    col_title += "\n\33[0m"
    # print("title :", col_title)
    return col_title
