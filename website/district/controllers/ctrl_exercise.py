from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils import timezone

from toolbox.exercise_generation.exercise_inspector import ExerciseInspector
from toolbox.utils.ansi_to_html import ansi_to_html
from toolbox.utils.exercise import get_exercise_details, get_exercise_write

from website.settings import LOGIN_URL


# return the view of an exercise
@login_required(login_url=LOGIN_URL)
def ctrl_exercise_details(request):
    # get the current user
    curr_user = request.user
    # get parameters
    ex_id = request.GET.get('ex', 0)

    response = get_exercise_details(curr_user, ex_id)
    if response["exit_code"] == 4:
        return HttpResponse("Please enter a valid number of exercise")
    elif response["exit_code"] == 3:
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

    response = get_exercise_write(curr_user, ex_id)
    if response["exit_code"] == 4:
        return HttpResponse("Please enter a valid number of exercise")
    elif response["exit_code"] == 3:
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
