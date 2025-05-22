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
        languages = [
            {'name': 'Python', 'url': 'https://www.python.org/doc/', 'img': '/static/images/logos/python.png'},
            {'name': 'JavaScript', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
             'img': '/static/images/logos/javascript.png'},
            {'name': 'Java', 'url': 'https://docs.oracle.com/en/java/', 'img': '/static/images/logos/java.png'},
            {'name': 'C++', 'url': 'https://isocpp.org/get-started', 'img': '/static/images/logos/cpp.png'},
            {'name': 'PHP', 'url': 'https://www.php.net/docs.php', 'img': '/static/images/logos/php.png'},
            {'name': 'C#', 'url': 'https://learn.microsoft.com/en-us/dotnet/csharp/',
             'img': '/static/images/logos/csharp.png'},
            {'name': 'C', 'url': 'https://en.cppreference.com/w/c/language', 'img': '/static/images/logos/c.png'},
            {'name': 'Dart', 'url': 'https://dart.dev/guides', 'img': '/static/images/logos/dart.png'},
            {'name': 'Rust', 'url': 'https://doc.rust-lang.org/book/', 'img': '/static/images/logos/rust.png'},
            {'name': 'Ruby', 'url': 'https://www.ruby-lang.org/en/documentation/',
             'img': '/static/images/logos/ruby.png'},
            {'name': 'Swift', 'url': 'https://swift.org/documentation/', 'img': '/static/images/logos/swift.png'},
            {'name': 'Kotlin', 'url': 'https://kotlinlang.org/docs/reference/',
             'img': '/static/images/logos/kotlin.png'},
            {'name': 'Perl', 'url': 'https://perldoc.perl.org/', 'img': '/static/images/logos/perl.png'},
            {'name': 'R', 'url': 'https://cran.r-project.org/manuals.html', 'img': '/static/images/logos/r.png'},
            {'name': 'Lua', 'url': 'https://www.lua.org/docs.html', 'img': '/static/images/logos/lua.png'},
            {'name': 'Prolog', 'url': 'https://www.swi-prolog.org/pldoc/doc_for?object=manual',
             'img': '/static/images/logos/prolog.png'},
        ]

        colors =[
        {"border": "border-blue-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(96,165,250,1)]"},
        {"border": "border-yellow-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(250,204,21,1)]"},
        {"border": "border-red-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(248,113,113,1)]"},
        {"border": "border-green-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(74,222,128,1)]"},
          {"border": "border-purple-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(192,132,252,1)]"},
          {"border": "border-pink-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(244,114,182,1)]"},
          {"border": "border-emerald-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(52,211,153,1)]"},
          {"border": "border-teal-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(45,212,191,1)]"},
          {"border": "border-indigo-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(129,140,248,1)]"},
            {"border": "border-orange-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(251,146,60,1)]"},

            {"border": "border-cyan-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(34,211,238,1)]"},
          {"border": "border-lime-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(163,230,53,1)]"},
          {"border": "border-sky-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(56,189,248,1)]"},
          {"border": "border-fuchsia-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(232,121,249,1)]"},
          {"border": "border-violet-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(167,139,250,1)]"},
            {"border": "border-rose-600", "shadow": "hover:shadow-[0_0_15px_4px_rgba(251,113,133,1)]"},

        ]

        # Combine language + color
        combined = []
        for i, lang in enumerate(languages):
            color = colors[i % len(colors)]
            combined.append({
                "name": lang["name"],
                "url": lang["url"],
                "img": lang["img"],
                "border": color["border"],
                "shadow": color["shadow"],
            })
        context = {
            'languages': combined
        }
        # Load view template
        template = loader.get_template('district/content/home.html')
        # render home page
        return HttpResponse(template.render(context, request))

def ctrl_about(request):
    context = {}
    template = loader.get_template('district/content/about.html')
    return HttpResponse(template.render(context, request))


def ctrl_error(request, err_msg):
    # dictionary for initial data with
    context = {"controller_error_message": err_msg}
    # Load view template
    template = loader.get_template('district/content/error.html')
    # render home page
    # TODO change HTML status code ? add a parameter (=exit_code) and add 300 to it to made a HTML status code ?
    return HttpResponse(template.render(context, request))
