from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from district.models import Language

# Create your views here.
def coding(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    template = loader.get_template('coding/languages.html')

    context["title"] = "List of handled programming languages"
    context["languages"] = Language.objects.all()


    return HttpResponse(template.render(context, request))

