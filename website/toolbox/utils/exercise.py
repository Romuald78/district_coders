from django.utils import timezone

from district.models.assessment import Assessment
from district.models.exercise import Exercise


# return a dict containing the wording of an exercise
def get_exercise(curr_user, ex_id):
    ex_obj = Exercise.objects.filter(id=ex_id, exo2test__test_id__assessment__groups__userdc=curr_user)
    if ex_id == 0 or len(ex_obj) == 0:
        return {"exit_code": 4}

    return {"exit_code": 0, "ex_obj": ex_obj}


def get_exercise_details(curr_user, ex_id):
    result = get_exercise(curr_user, ex_id)
    if result["exit_code"] != 0:
        return result
    ex_obj = result["ex_obj"]
    all_asse = Assessment.objects.filter(groups__userdc=curr_user, test_id__exo2test__exercise_id=ex_id)
    # check if the exo is only in past assessments
    ended = True
    for asse in all_asse:
        if timezone.now().__lt__(asse.end_time) or timezone.now().__le__(asse.start_time):
            ended = False
    if not ended:
        return {"exit_code": 3}

    return {"exit_code": 0, "wording": ex_obj.first()}


def get_exercise_write(curr_user, ex_id):
    result = get_exercise(curr_user, ex_id)
    if result["exit_code"] != 0:
        return result
    ex_obj = result["ex_obj"]

    # all assessment must be in training mode OR at least one must be in process
    # get all assessment of the user group containing the exercise
    all_asse = Assessment.objects.filter(
        groups__userdc=curr_user,
        test_id__exo2test__exercise_id=ex_id,
        end_time__gt=timezone.now(),
        training_time__lte=timezone.now()
    )
    if len(all_asse) == 0:
        return {"exit_code": 3}
    all_in_future = True
    for asse in all_asse:
        if asse.start_time.__le__(timezone.now()) or asse.end_time.__le__(timezone.now()):
            all_in_future = False

    if all_in_future:
        return {"exit_code": 3}

    return {"exit_code": 0, "wording": ex_obj.first()}
