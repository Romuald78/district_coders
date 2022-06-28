from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from district.controllers.ctrl_main import ctrl_error
from toolbox.utils.assessment import get_asse_exercises

from website.settings import LOGIN_URL


# display the list of exercises in an assessment
@login_required(login_url=LOGIN_URL)
def ctrl_asse_details(request, id_asse):
    result = get_asse_exercises(request, id_asse)
    if result["exit_code"] != 0:
        return ctrl_error(request, result["err_msg"][1])

    # Load view template
    template = loader.get_template('district/exercisesAssess.html')

    # Use context in the template and render response view
    return HttpResponse(template.render(result, request))
