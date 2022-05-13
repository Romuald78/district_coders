from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from district.models import Language

# Create your views here.
def coding(request):
    # Get parameters from request (e.g. : form field values)
    # either with the GET method or the POST method
    print(request.GET)
    print(request.POST)

    # dictionary for initial data with
    # field names as keys
    context = {}

    # Load view template
    template = loader.get_template('coding/languages.html')

    # Create context dictionary
    # Use any needed models for that
    context["title"] = "List of handled programming languages"
    context["languages"] = Language.objects.all()

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))

