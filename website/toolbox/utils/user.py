import traceback
from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config.secure import email_cnf
from toolbox.users.tokens import account_activation_token
from website import settings

def send_confirm_email(request, user):
    print(f"[DEBUG] Sending email to {user.email}")
    current_site = get_current_site(request)
    subject = 'Please Activate Your Account'
    from_email = email_cnf.EMAIL_HOST_USER
    to_email = [user.email]

    # Creates the HTML message
    html_content = render_to_string('registration/mails/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'year': datetime.now().year,  # si tu l'utilises dans le footer
    })

    # Plain text version (fallback)
    text_content = f"""
        Hello {user.username},
        
        Please confirm your email by clicking the link below:
        
        http://{current_site.domain}/accounts/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{account_activation_token.make_token(user)}/
        """

    # Création de l'email multipart
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()