
# display the list of exercises in an assessment
import traceback

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from district.models.assessment import Assessment
from district.models.exo2test import Exo2Test
from district.models.exotest2lang import ExoTest2Lang
from district.models.testresult import TestResult
from secure import error_message_cnf
from toolbox.utils.assessment import is_asse_available
from toolbox.utils.exercise import is_exo_triable
from website import settings
from website.settings import LOGIN_URL


# check if a testresult exists for a certain user, assessment and exotest2lang
# create one if not
@login_required(login_url=LOGIN_URL)
def ctrl_json_testresult_exists(request):
    try:
        # get params
        curr_user = request.user
        asse_id = int(request.POST.get("asse_id", 0))
        ex2tst_id = int(request.POST.get("ex2tst_id", 0))
        lang_id = int(request.POST.get("lang_id", 0))

        if asse_id == 0 or ex2tst_id == 0 or lang_id == 0:
            return JsonResponse({"exit_code": 4, "err_msg": error_message_cnf.TESTRESULT_NOT_FOUND})

        # check if the assessment is reachable by the user
        asse_objs = Assessment.objects.filter(id=asse_id)
        if len(asse_objs.all()) == 0:
            return JsonResponse({"exit_code": 4, "err_msg": error_message_cnf.ASSESSMENT_NOT_FOUNT})
        result_asse = is_asse_available(asse_objs)
        if not result_asse[0]["is_available"]:
            return JsonResponse({"exit_code": 3, "err_msg": result_asse[0]["not_available_msg"]})

        # check if the exercise is triable by the user
        all_exo2test = Exo2Test.objects.filter(id=ex2tst_id) # one result
        if len(all_exo2test.all()) == 0:
            return JsonResponse({"exit_code": 4, "err_msg": error_message_cnf.EXERCISE_NOT_FOUND})
        result_exo = is_exo_triable(curr_user, asse_objs.first(), all_exo2test)
        exo2test_id = all_exo2test.first().id
        if not result_exo[exo2test_id]["is_triable"]:
            return JsonResponse({"exit_code": 3, "err_msg": result_asse[exo2test_id]["not_triable_msg"]})

        # check if a test result already exist
        test_result = TestResult.objects.filter(
            assessment_id=asse_id,
            exo_test2lang__exo2test=ex2tst_id,
            exo_test2lang__lang=lang_id,
            user_id=curr_user)
        if len(test_result.all()) == 0:
            # do not exist, create it
            new_test_result = TestResult()
            new_test_result.user = curr_user
            new_test_result.assessment = asse_objs.first()
            new_test_result.exo_test2lang = ExoTest2Lang.objects.get(exo2test_id=ex2tst_id, lang_id=lang_id)

            new_test_result.save()

        return JsonResponse({"exit_code": 0})
    except:
        if settings.DEBUG:
            print(traceback.print_exc())
        return JsonResponse({})
