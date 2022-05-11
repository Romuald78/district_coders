from django.shortcuts import render
from django.http import HttpResponse

from district.models import Language

# Create your views here.
def coding(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    response = Language.objects.all()
    return HttpResponse(response, content_type='application/json')

