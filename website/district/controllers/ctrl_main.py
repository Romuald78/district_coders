import os
from django.utils import timezone

from django.http import HttpResponse, JsonResponse
from django.template import loader

from classes.exercise_generation.exercise_inspector import ExerciseInspector
from classes.utils.ansi_to_html import ansi_to_html
from classes.utils.assessment import ctrl_current_asse, ctrl_past_asse, ctrl_future_asse

from website.settings import MEDIA_ROOT
from django.shortcuts import redirect

def ctrl_home(request):

    if request.user.is_authenticated:
        # dictionary for initial data with
        context = {}
        # Load view template
        template = loader.get_template('district/content/user_home.html')
        # Retrieve all assessments data
        context["training"]   = ctrl_past_asse(request)
        context["inprogress"] = ctrl_current_asse(request)
        context["future"]     = ctrl_future_asse(request)
        # render home page
        return HttpResponse(template.render(context, request))

    else:
        # dictionary for initial data with
        context = {}
        # Load view template
        template = loader.get_template('district/content/home.html')
        # render home page
        return HttpResponse(template.render(context, request))




def test_view(request):
    user_id = 1
    ex_id = 4
    lang_id = 1
    with open(os.path.join(MEDIA_ROOT, "user_codes", "user004.c")) as f:
        code = f.read()

    toto = ExerciseInspector(user_id, ex_id, lang_id, code)
    (exit_code, stdout, stderr) = toto.process()
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
        "stderr": stderr
    }

    #return HttpResponse(result)
    return JsonResponse(dico_json_response)
