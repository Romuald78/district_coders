import json
import traceback

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils import timezone

from config.constants.error_message_cnf import ERROR_CODE_ACCESS, ERROR_CODE_NOT_FOUND, ERROR_CODE_PARAMS, \
    ERROR_CODE_OK, ERROR_CODE_COMPILE, COMPILE_ERROR, ERROR_CODE_IMPOSSIBLE, ERROR_CODE_UNSUPPORTED
from district.controllers.ctrl_main import ctrl_error
from district.controllers.ctrl_testresult import ctrl_json_testresult_exists
from district.models.assessment import Assessment
from district.models.exotest2lang import ExoTest2Lang
from config.constants import default_value_cnf, error_message_cnf
from toolbox.exercise_generation.exercise_inspector import ExerciseInspector
from toolbox.utils.ansi_to_html import ansi_to_html
from toolbox.utils.assessment import is_date_current
from toolbox.utils.exercise import get_exercise_details, get_exercise_write, get_title_console, get_exercise_stat
from toolbox.utils.testresult import get_testresult
from website import settings

from website.settings import LOGIN_URL


# return the view of an exercise
@login_required(login_url=LOGIN_URL)
def ctrl_exercise_details(request):
    # get the current user
    curr_user = request.user
    # get parameters
    ex2tst_id = int(request.GET.get('extest', 0))
    asse_id = int(request.GET.get('asse', 0))

    response = get_exercise_details(curr_user, ex2tst_id, asse_id)
    if response["exit_code"] != ERROR_CODE_OK:
        return ctrl_error(request, response["err_msg"][1])

    # dictionary for initial data
    context = {}
    # Load view template
    template = loader.get_template('district/exercisewording.html')
    # get current assessment
    context["ex2tst"] = response["ex2tst_obj"]
    context["is_triable"] = response["is_triable"]
    # convert the list of languages into dict of lang_id -> {String name, String default_code, int result_test, int result_train}
    languages = {}
    for extstlng in response["ex_tst_lng"]:
        languages[extstlng.lang.id] = {
            "name": extstlng.lang.name,
            "default_code": extstlng.lang.default_code,
            "result_test": int(0 if extstlng.nb_test_try == 0 else 100*extstlng.nb_test_pass/extstlng.nb_test_try),
            "result_train": int(0 if extstlng.nb_train_try == 0 else 100*extstlng.nb_train_pass/extstlng.nb_train_try)}
    context["languages"] = languages
    context["asse_id"] = asse_id

    # adding testresult stat
    context["testresults"] = get_testresult(curr_user.id, asse_id, response["ex_tst_lng"])

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def ctrl_exercise_write(request):
    # get the current user
    curr_user = request.user
    # get parameters
    ex2tst_id = int(request.GET.get('extest', 0))
    asse_id = int(request.GET.get('asse', 0))

    response = get_exercise_write(curr_user, ex2tst_id, asse_id)
    if response["exit_code"] != ERROR_CODE_OK:
        return ctrl_error(request, response["err_msg"][1])

    # dictionary for initial data
    context = {}
    # Load view template
    template = loader.get_template('district/exercise_write.html')

    # get current assessment
    context["ex2tst"] = response["ex2tst_obj"]

    if len(response["ex_tst_lng"]) == 0:
        return ctrl_error(request, error_message_cnf.LANGUAGE_NOT_AVAILABLE)
    # TODO : check ALL the languages (not only the very first ([0])
    result = get_exercise_stat(curr_user, ex2tst_id, asse_id, response["ex_tst_lng"][0].lang_id)
    if result["exit_code"] != ERROR_CODE_OK:
        return ctrl_error(request, result["err_msg"][1])

    context["languages"] = result["languages"]
    context["asse_id"] = asse_id
    context["max_raw_code"] = default_value_cnf.MAX_LENGTH_USER_RAW_CODE

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def ctrl_json_exercise_inspect(request):
    # prepare answer
    dico_json_response = {
        "title": ansi_to_html(get_title_console()),
        "time_stamp": str(timezone.now()), # TODO useless ???
        "exit_code": None,
        "err_msg": "",
        "stdout": "",
        "stderr": "",
    }

    try:
        # get parameters
        user_id = request.user.id
        ex2tst_id = int(request.POST.get('ex2tst_id', 0))
        lang_id = int(request.POST.get('lang_id', 0))
        user_code = request.POST.get('raw_code', "")
        asse_id = int(request.POST.get("asse_id", 0))

        # verif the code is short enough
        if len(user_code.encode("UTF-8")) > default_value_cnf.MAX_LENGTH_USER_RAW_CODE:
            dico_json_response["exit_code"] = ERROR_CODE_ACCESS
            dico_json_response["err_msg"]   = error_message_cnf.USER_RAW_CODE_TOO_BIG
            return JsonResponse(dico_json_response)

        # make sure the user is able to access to the inspection
        response = get_exercise_write(user_id, ex2tst_id, asse_id)
        if response["exit_code"] != ERROR_CODE_OK:
            dico_json_response["exit_code"] = response["exit_code"]
            dico_json_response["err_msg"]   = response["err_msg"]
            return JsonResponse(dico_json_response)

        # make sure the language selected is available for this exo2test
        language_missing = True
        for i in response["ex_tst_lng"]:
            if i.lang.id == lang_id:
                language_missing = False
        if language_missing:
            dico_json_response["exit_code"] = ERROR_CODE_NOT_FOUND
            dico_json_response["err_msg"]   = error_message_cnf.LANGUAGE_NOT_AVAILABLE
            return JsonResponse(dico_json_response)

        # Retrieve the exotest2lang
        queryset_exotest2lang = ExoTest2Lang.objects.filter(exo2test_id=ex2tst_id, lang_id=lang_id)
        if not queryset_exotest2lang.exists():
            dico_json_response["exit_code"] = ERROR_CODE_NOT_FOUND
            dico_json_response["err_msg"]   = error_message_cnf.EXOTEST2LANG_NOT_FOUND
            return JsonResponse(dico_json_response)

        # proceed the inspection
        exotest2lang = queryset_exotest2lang.first()
        ex_insp = ExerciseInspector(user_id, response["ex2tst_obj"].exercise.id, lang_id, user_code, response["ex2tst_obj"].solve_percentage_req, exotest2lang.exec_timeout)
        (exit_code, stdout, stderr) = ex_insp.process()

        # Check compilation (depending on language)
        if exit_code == ERROR_CODE_COMPILE:
            dico_json_response["exit_code"] = exit_code
            dico_json_response["err_msg"] = COMPILE_ERROR
            return JsonResponse(dico_json_response)

        # Get exo percentage from exit_code
        exo_perc = exit_code/2

        # saving result into ExoTest2Lang and TestResult
        json_response = ctrl_json_testresult_exists(request)
        dict_response = json.loads(json_response.content)
        if dict_response["exit_code"] != ERROR_CODE_OK:
            dico_json_response["exit_code"] = ERROR_CODE_PARAMS
            dico_json_response["err_msg"]   = dict_response["err_msg"] # Missing testResult
            return JsonResponse(dico_json_response)
        else:
            testresult = get_testresult(user_id, asse_id, queryset_exotest2lang)[0]["testresult_obj"]

        # is assessment in process or not
        asse_obj = Assessment.objects.get(id=asse_id)
        if is_date_current(asse_obj):
            testresult.nb_test_try += 1
            exotest2lang.nb_test_try += 1

            # according to testresult.solve_percentage
            if exo_perc >= 0 and exo_perc <= 100: # exercise has been processed
                # update max result
                if testresult.solve_percentage < exo_perc:
                    testresult.solve_percentage = exo_perc
                    testresult.solve_code = user_code
                    testresult.solve_time = timezone.now()
                # if the actual solve percentage is above the required limit
                # the test can be count as passed (so the same user can pass this exo several times)
                # it is not compulsory to have 100% : just the solve_percentage_req value or above
                if testresult.solve_percentage >= response["ex2tst_obj"].solve_percentage_req:
                    exotest2lang.nb_test_pass += 1
            # NO else : the exit_code is an error and not a test_percentage
        else:
            exotest2lang.nb_train_try += 1
            if exit_code >= response["ex2tst_obj"].solve_percentage_req:# success
                exotest2lang.nb_train_pass += 1

        exotest2lang.save()
        testresult.save()

        # exit_code : int
        # stdout : str
        # stderr : str
        dico_json_response["exit_code"] = exit_code
        dico_json_response["stdout"]    = ansi_to_html(stdout)
        dico_json_response["stderr"]    = ansi_to_html(stderr)
        return JsonResponse(dico_json_response)
    except AttributeError as atrerr:
        if settings.DEBUG:
            print(traceback.print_exc())
        # raise AttributeError("Language program not found") from atrerr
        dico_json_response["exit_code"] = ERROR_CODE_UNSUPPORTED
        dico_json_response["err_msg"] = error_message_cnf.LANGUAGE_NOT_SUPPORTED
        return JsonResponse(dico_json_response)
    except ():
        if settings.DEBUG:
            print(traceback.print_exc())
        return JsonResponse({})


@login_required(login_url=LOGIN_URL)
def ctrl_json_exercise_get_stat(request):
    try:
        # get params
        curr_user = request.user
        ex2tst_id = int(request.POST.get('ex2tst_id', 0))
        asse_id = int(request.POST.get("asse_id", 0))
        lang_id = int(request.POST.get('lang_id', 0))

        if asse_id == 0 or ex2tst_id == 0 or lang_id == 0:
            return JsonResponse({"exit_code": ERROR_CODE_PARAMS, "err_msg": error_message_cnf.ASSESSMENT_NOT_FOUNT})

        # response = get_exercise_details(curr_user, ex2tst_id, asse_id)
        # if response["exit_code"] != ERROR_CODE_OK:
        #     return JsonResponse({"exit_code": response["exit_code"], "err_msg": response["err_msg"]})

        result = get_exercise_stat(curr_user, ex2tst_id, asse_id, lang_id)

        return JsonResponse(result)
    except ():
        if settings.DEBUG:
            print(traceback.print_exc())
        return JsonResponse({})
