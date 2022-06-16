from django.utils import timezone

from district.models.assessment import Assessment
from district.models.exercise import Exercise


# return a dict containing the wording of an exercise
def get_exercise(curr_user, ex_id):
    ex_obj = Exercise.objects.filter(id=ex_id, exo2test__test_id__assessment__groups__userdc=curr_user)
    if ex_id == 0 or len(ex_obj) == 0:
        return {"exit_code": 4}

    # all assessment must be in training mode OR at least one must be in process
    # get all assessment of the user group containing the exercise
    all_asse = Assessment.objects.filter(groups__userdc=curr_user, test_id__exo2test__exercise_id=ex_id)
    in_process = False
    in_training = True
    for asse in all_asse:
        if asse.start_time.__le__(timezone.now()) and timezone.now().__lt__(asse.end_time):
            in_process = True
        if not timezone.now().__ge__(asse.training_time):
            in_training = False

    if not in_process and not in_training:
        return {"exit_code": 3}

    return {"exit_code": 0, "wording": ex_obj.first()}
