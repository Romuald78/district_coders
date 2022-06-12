import os

from django.http import HttpResponse
from django.template import loader

from classes.exercise_generation.exercise_inspector import ExerciseInspector
from district.models.language import Language

# Create your views here.
from website.settings import MEDIA_ROOT, MEDIA_URL


def main_view(request):
    # Get parameters from request (e.g. : form field values)
    # either with the GET method or the POST method
    # print(request.GET)
    # print(request.POST)

    # dictionary for initial data with
    # field names as keys
    context = {}

    # Load view template
    template = loader.get_template('district/base.html')

    # Create context dictionary
    # Use any needed models for that
    context["page_title"] = "District Coders"
    context["title"] = "List of handled programming languages"
    context["languages"] = Language.objects.all().order_by('name')
    context["MEDIA_URL"] = MEDIA_URL

    # Get variable from session (with default value)
    nb_visits = request.session.get('nb_visits', 0)
    request.session['nb_visits'] = nb_visits + 1
    context['nb_visits'] = nb_visits

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


def test_view(request):
    user_id = 1
    ex_id = 4
    lang_id = 1
    with open(os.path.join(MEDIA_ROOT, "user_codes", "user004.c")) as f:
        code = f.read()

    toto = ExerciseInspector(user_id, ex_id, lang_id, code)
    result = toto.process()
    return HttpResponse(result)
