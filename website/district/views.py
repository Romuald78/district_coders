from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from district.models import Language

# Create your views here.
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

    # Get variable from session (with default value)
    nb_visits = request.session.get('nb_visits', 0)
    request.session['nb_visits'] = nb_visits + 1
    context['nb_visits'] = nb_visits

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))

