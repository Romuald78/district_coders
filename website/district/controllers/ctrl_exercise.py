from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils import timezone

from classes.exercise_generation.exercise_inspector import ExerciseInspector
from classes.utils.ansi_to_html import ansi_to_html
from district.models.assessment import Assessment
from district.models.exercise import Exercise


from website.settings import LOGIN_URL


# return a dict containing the wording of an exercise
def get_exercise(curr_user, ex_id):
    ex_obj = Exercise.objects.filter(id=ex_id, exo2test__test_id__assessment__groups__userdc=curr_user)
    if ex_id == 0 or len(ex_obj) == 0:
        return {"exit_code": 404}

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
        return {"exit_code": 403}

    return {"exit_code": 0, "wording": ex_obj.first()}


# return the view of an exercise
@login_required(login_url=LOGIN_URL)
def ctrl_exercise_details(request):
    # get the current user
    curr_user = request.user
    # get parameters
    ex_id = request.GET.get('ex', 0)

    response = get_exercise(curr_user, ex_id)
    if response["exit_code"] == 404:
        return HttpResponse("Please enter a valid number of exercise")
    elif response["exit_code"] == 403:
        return HttpResponse("Access denied")

    # dictionary for initial data
    context = {}
    # Load view template
    template = loader.get_template('district/exercisewording.html')
    # get current assessment
    context["wording"] = response["wording"]

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def ctrl_exercise_write(request):
    # get the current user
    curr_user = request.user
    # get parameters
    ex_id = request.GET.get('ex', 0)

    response = get_exercise(curr_user, ex_id)
    if response["exit_code"] == 404:
        return HttpResponse("Please enter a valid number of exercise")
    elif response["exit_code"] == 403:
        return HttpResponse("Access denied")

    # dictionary for initial data
    context = {}
    # Load view template
    template = loader.get_template('district/exercise_write.html')
    # get current assessment
    context["wording"] = response["wording"]

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def ctrl_json_exercise_inspect(request):
    # get parameters
    user_id = request.user.id
    ex_id = request.POST.get('ex_id', 0)
    lang_id = request.POST.get('lang_id', 0)
    user_code = request.POST.get('raw_code', "")

    ex_insp = ExerciseInspector(user_id, ex_id, lang_id, user_code)
    (exit_code, stdout, stderr) = ex_insp.process()

    # ex_id : int
    # user_id : int
    # timestamp (date et heure de début de la requete (reception de la requete))
    # exit_code : int
    # stdout : str
    # stderr : str
    dico_json_response = {
        "ex_id": ex_id,
        "user_id": user_id,
        "timestamp": timezone.now(),
        "exit_code": exit_code,
        "stdout": ansi_to_html(stdout),
        "stderr": ansi_to_html(stderr)
    }

    return JsonResponse(dico_json_response)
