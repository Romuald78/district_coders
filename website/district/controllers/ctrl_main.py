import traceback

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string

from config.secure import email_cnf
from toolbox.utils.assessment import get_current_asse, get_past_asse, get_future_asse, is_asse_available, \
    detect_assess_overlaps


def ctrl_home(request):

    if request.user.is_authenticated:
        # dictionary for initial data with
        context = {}
        # Load view template
        template = loader.get_template('district/content/user_home.html')
        # Retrieve all assessments data
        past    = is_asse_available(get_past_asse(request))
        current = is_asse_available(get_current_asse(request))
        future  = is_asse_available(get_future_asse(request))
        # Process all assessments and try to find a collision
        # it modifies the previous dict adding
        # a 'collisions' field (list of other asses ids)
        detect_assess_overlaps(past, current, future)
        # render home page
        context["training"]   = past
        context["inprogress"] = current
        context["future"]     = future
        return HttpResponse(template.render(context, request))

    else:
        # dictionary for initial data with
        context = {}
        # Load view template
        template = loader.get_template('district/content/home.html')
        # render home page
        return HttpResponse(template.render(context, request))


def ctrl_error(request, err_msg):
    # dictionary for initial data with
    context = {"err_msg": err_msg}
    # Load view template
    template = loader.get_template('district/content/error.html')
    # render home page
    # TODO change HTML status code ? add a parameter (=exit_code) and add 300 to it to made a HTML status code ?
    return HttpResponse(template.render(context, request), status=302)
