from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from toolbox.users.tokens import account_activation_token


def send_confirm_email(request, user):
    # sending email to confirm user's email
    current_site = get_current_site(request)
    subject = 'Please Activate Your Account'
    # load a template like get_template()
    # and calls its render() method immediately.
    message = render_to_string('registration/mails/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        # method will generate a hash value with user related data
        'token': account_activation_token.make_token(user),
    })

    user.email_user(subject, message)
