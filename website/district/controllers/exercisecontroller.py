from django.http import HttpResponse
from django.template import loader

from district.models.assessment import Assessment
from district.models.exercise import Exercise


def get_exercise(request):
    # get parameters
    id_ex = request.GET.get('ex', 0)
    if id_ex == 0:
        return HttpResponse("Please enter a valid number of exercise")

    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/exercisecode.html')

    # get current assessment
    context["wording"] = Exercise.objects.filter(id=id_ex)

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


# TODO
def get_verify(request):
    # get parameters
    id_ex = request.POST.get('idex', 0)
    if id_ex == 0:
        return HttpResponse("Please enter a valid number of exercise")

    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/exercisecode.html')

    # get current assessment
    context["wording"] = Exercise.objects.filter(id=id_ex)

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))
