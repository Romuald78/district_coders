from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils import timezone

from district.models.assessment import Assessment
from district.models.exotest2lang import ExoTest2Lang
from toolbox.exercise_generation.exercise_inspector import ExerciseInspector
from toolbox.utils.ansi_to_html import ansi_to_html
from toolbox.utils.assessment import is_date_current
from toolbox.utils.exercise import get_exercise_details, get_exercise_write

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
    if response["exit_code"] != 0:
        if response["exit_code"] == 4:
            return HttpResponse("Please enter a valid number of exercise")
        elif response["exit_code"] == 3:
            return HttpResponse("Access denied")
        else:
            return HttpResponse("Unknown error")

    # dictionary for initial data
    context = {}
    # Load view template
    template = loader.get_template('district/exercisewording.html')
    # get current assessment
    context["ex2tst"] = response["ex2tst_obj"]
    context["asse_id"] = asse_id

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
    if response["exit_code"] != 0:
        if response["exit_code"] == 4:
            return HttpResponse("Please enter a valid number of exercise")
        elif response["exit_code"] == 3:
            return HttpResponse("Access denied")
        else:
            return HttpResponse("Unknown error")

    # dictionary for initial data
    context = {}
    # Load view template
    template = loader.get_template('district/exercise_write.html')
    # get current assessment
    context["ex2tst"] = response["ex2tst_obj"]
    # convert the list of languages into dict of lang_id -> {String name, String default_code}
    languages = {}
    for lang in response["lang_objs"]:
        languages[lang.id] = {"name": lang.name, "default_code": lang.default_code}
    context["languages"] = languages
    context["asse_id"] = asse_id

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def ctrl_json_exercise_inspect(request):
    # get parameters
    user_id = request.user.id
    ex2tst_id = int(request.POST.get('ex2tst_id', 0))
    lang_id = int(request.POST.get('lang_id', 0))
    user_code = request.POST.get('raw_code', "")
    asse_id = int(request.POST.get("asse_id", 0))

    # make sure the user is able to access to the inspection
    response = get_exercise_write(user_id, ex2tst_id, asse_id)
    if response["exit_code"] != 0:
        if response["exit_code"] == 4:
            return HttpResponse("Please enter a valid number of exercise")
        elif response["exit_code"] == 3:
            return HttpResponse("Access denied")
        else:
            return HttpResponse("Unknown error")

    # make sure the language selected is available for this exo2test
    language_missing = True
    for i in response["lang_objs"]:
        if i.id == lang_id:
            language_missing = False
    if language_missing:
        return HttpResponse("Please enter a valid programming language")


    # process to the inspection
    ex_insp = ExerciseInspector(user_id, response["ex2tst_obj"].exercise_id.id, lang_id, user_code)
    (exit_code, stdout, stderr) = ex_insp.process()

    # # saving result into ExoTest2Lang
    # exotest2lang = ExoTest2Lang.objects.get(exo2test_id=ex2tst_id, lang_id=lang_id)
    # # is current of not
    # if is_date_current(Assessment.objects.get(id=asse_id)):
    #     exotest2lang.nb_test_try += 1
    #     if exit_code == 0: # success
    #         exotest2lang.nb_test_pass += 1
    # else:
    #     exotest2lang.nb_train_try += 1
    #     if exit_code == 0:  # success
    #         exotest2lang.nb_train_pass += 1
    #
    # exotest2lang.save()
    print("oh nice nice")

    # ex_id : int
    # user_id : int
    # timestamp (date et heure de début de la requete (reception de la requete))
    # exit_code : int
    # stdout : str
    # stderr : str
    dico_json_response = {
        "ex_id": response["ex2tst_obj"].exercise_id.id,
        "user_id": user_id,
        "timestamp": timezone.now(),
        "exit_code": exit_code,
        "stdout": ansi_to_html(stdout),
        "stderr": ansi_to_html(stderr)
    }

    return JsonResponse(dico_json_response)
