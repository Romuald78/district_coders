from django.http import HttpResponse
from django.template import loader

from district.models.assessment import Assessment
from district.models.exercise import Exercise


# return the view of an exercise
def get_exercise(request):
    # get parameters
    id_ex = request.GET.get('ex', 0)
    if id_ex == 0 or len(Exercise.objects.filter(id=id_ex)) == 0:
        return HttpResponse("Please enter a valid number of exercise")

    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/exercisecode.html')

    # get current assessment
    context["wording"] = Exercise.objects.filter(id=id_ex)

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))


def get_verify(request):
    # get parameters
    user_id = 1 #TODO à remplacer
    ex_id = request.POST.get('ex_id', 0)
    lang_id = 1
    with open(os.path.join(MEDIA_ROOT, "user_codes", "user004.c")) as f:
        code = f.read()

    toto = ExerciseInspector(user_id, ex_id, lang_id, code)
    result = toto.process()
    return HttpResponse(result)


    if id_ex == 0 or len(Exercise.objects.filter(id=id_ex)) == 0:
        return HttpResponse("Please enter a valid number of exercise")

    # dictionary for initial data
    context = {}

    # Load view template
    template = loader.get_template('district/exercisecode.html')

    # get current assessment
    context["wording"] = Exercise.objects.filter(id=id_ex)

    # Use context in the template and render response view
    return HttpResponse(template.render(context, request))
