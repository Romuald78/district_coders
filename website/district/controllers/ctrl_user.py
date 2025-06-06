import os.path
import shutil
import traceback
from datetime import datetime
from logging import currentframe

from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.core.validators import validate_email
from django.db.models import Q
from django.db.models.fields.files import ImageFieldFile, FieldFile, ImageField
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes

from config.constants.error_message_cnf import ERROR_CODE_CONFLICT, ERROR_CODE_NOT_FOUND, ERROR_CODE_PARAMS, \
    ERROR_CODE_OK, ERROR_CODE_ACCESS
from config.secure import email_cnf
from district.controllers.ctrl_main import ctrl_error
from district.models.user import UserDC, user_icon_upload_to
from config.constants import error_message_cnf
from toolbox.users.signup import SignupForm
from district.models.group import GroupDC
from toolbox.users.tokens import account_activation_token
from toolbox.users.update import UserUpdateForm
from toolbox.utils.user import send_confirm_email
from website import settings
from website.settings import LOGIN_URL, DEFAULT_GROUP_KEY, MEDIA_ROOT


@login_required(login_url=LOGIN_URL)
def ctrl_user_profile(request):
    # get the user currently logged and groups that he belongs to
    curr_user = request.user
    context = {"user": curr_user}

    # Load view template
    template = loader.get_template('district/user_profile.html')

    return HttpResponse(template.render(context, request))

def upload_default_icon(user):
    static_icon_path = os.path.join(MEDIA_ROOT, "..", "district", "static", "images", "logos", "avatar.png")
    usr_icon_path = user_icon_upload_to(user, '')
    shutil.copy(static_icon_path, os.path.join(MEDIA_ROOT, usr_icon_path))
    user.icon = ImageFieldFile(user, user.icon, usr_icon_path)

# No login required to sign up (indeed)
def ctrl_user_signup(request):
    form = SignupForm(request.POST, request.FILES)
    # Get default group
    groups = GroupDC.objects.filter(register_key=DEFAULT_GROUP_KEY)
    if request.method == "POST":
        if form.is_valid() and groups.exists():
            # retrieve form data
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.groups.add(GroupDC.objects.get(register_key=DEFAULT_GROUP_KEY))
            if form.cleaned_data.get('icon'):
                user.icon = form.cleaned_data.get('icon')
            else:
                upload_default_icon(user)
            # Check email is not empty
            if user.email is not None and user.email != '':
                # confirmation email
                user.is_active = False
                user.save()
                return redirect(reverse('email_change_confirm', kwargs={"user_id": user.id}))
    else:
        form = SignupForm()

    context = {'form': form}
    # Load view template
    template = loader.get_template('registration/signup.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url=LOGIN_URL)
def ctrl_json_user_register(request):
    try:
        # get parameters from request
        register_key = request.POST.get("register_key", "")
        user_id = request.user.id

        if len(register_key) == 0 or user_id == 0:
            return JsonResponse({"exit_code": ERROR_CODE_PARAMS, "err_msg": error_message_cnf.GROUP_REGISTER_EMPTY_KEY})

        # check if the key exists. In this case, get the id of the group concerned
        groups = GroupDC.objects.filter(register_key=register_key)
        if not groups.exists():
            return JsonResponse({"exit_code": ERROR_CODE_NOT_FOUND, "err_msg": error_message_cnf.GROUP_REGISTER_INVALID_KEY})

        if GroupDC.objects.filter(id=groups.first().id, userdc=user_id).exists():
            return JsonResponse({"exit_code": ERROR_CODE_CONFLICT, "err_msg": error_message_cnf.GROUP_REGISTER_ALREADY_IN})

        # link the group to the user
        user_obj = UserDC.objects.get(id=user_id)
        user_obj.groups.add(groups.first())
        user_obj.save()

        # return a dictionary
        return JsonResponse({"exit_code": ERROR_CODE_OK})
    except:
        if settings.DEBUG:
            print(traceback.print_exc())
        return JsonResponse({})


# return a dict of {
#     Dict group_obj {
#       String name
#       String icon
#       String description
#     }
#     List of String group_users : name of users in a group
@login_required(login_url=LOGIN_URL)
def ctrl_json_user_groups(request):
    try:
        user_id = request.user.id
        all_groups = GroupDC.objects.filter(userdc=user_id)

        groups_users = {}
        for g in all_groups:
            user_name = [user.username for user in g.userdc_set.all() if user.id != user_id]
            if g.id not in groups_users:
                group_dict = {"name": g.name, "icon": str(g.icon), "description": g.description}
                groups_users[g.id] = {"group_obj": group_dict, "group_users": user_name}
            else:
                groups_users[g.id]["group_users"] += user_name

        return JsonResponse(groups_users)
    except:
        if settings.DEBUG:
            print(traceback.print_exc())
        return JsonResponse({})


@login_required(login_url=LOGIN_URL)
def ctrl_user_update(request, user_id):
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            if form.cleaned_data.get('icon'):
                user.icon = form.cleaned_data.get('icon')
            else:
                upload_default_icon(user)
                # user.icon = ImageFieldFile(user, field=ImageField(blank=True, upload_to=user_icon_upload_to, default=user_icon_default), name=os.path.join("..", "static", "images", "logos", "logo_district_128.png"))
            user.description = form.cleaned_data.get('description')
            user = form.save()
            user.refresh_from_db()
            return redirect('/accounts/profile/')
    else:
        form = UserUpdateForm(instance=user)

    context = {'form': form}
    # Load view template
    template = loader.get_template('registration/update.html')
    return HttpResponse(template.render(context, request))


def ctrl_user_validate_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserDC.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserDC.DoesNotExist):
        user = None
        # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.previous_email = None
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return ctrl_error(request, error_message_cnf.EMAIL_CONFIRM_ERROR[1])


def ctrl_email_verification(request, user_id):
    try:
        curr_user = UserDC.objects.get(id=user_id)
    except UserDC.DoesNotExist:
        curr_user = None

    if curr_user is not None and not curr_user.is_active:
        context = {}
        context["user_id"] = curr_user.id
        context["email"] = curr_user.email
        template = loader.get_template('registration/send_email_verification.html')
        return HttpResponse(template.render(context, request))

    else:
        return ctrl_error(request, error_message_cnf.EMAIL_ALREADY_CONFIRM[1])


def ctrl_json_sending_email(request):
    user_id = int(request.POST.get("user_id", 0))
    try:
        curr_user = UserDC.objects.get(id=user_id)
    except UserDC.DoesNotExist:
        curr_user = None

    if curr_user is not None and not curr_user.is_active:
        send_confirm_email(request, curr_user)
        return JsonResponse({"exit_code": ERROR_CODE_OK})
    else:
        return JsonResponse({"exit_code": ERROR_CODE_ACCESS, "err_msg": error_message_cnf.EMAIL_ALREADY_CONFIRM})


def ctrl_password_reset_request(request):
    logout(request)
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = UserDC.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/mails/reset_password_email.html"

                    c = {
                        "email": user.email,
                        "domain": get_current_site(request).domain,
                        "site_name": "District Coders",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "https" if request.is_secure() else "http",
                        "year": datetime.now().year,
                    }

                    html_content = render_to_string(email_template_name, c)
                    text_content = strip_tags(html_content)  # facultatif, pour fallback texte

                    email = EmailMultiAlternatives(
                        subject,
                        text_content,  # texte brut fallback
                        email_cnf.EMAIL_HOST_USER,
                        [user.email]
                    )
                    email.attach_alternative(html_content, "text/html")  # ajoute le HTML

                    try:
                        email.send(fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    return redirect("/accounts/password_reset/done/")

    # GET ou formulaire invalide
    password_reset_form = PasswordResetForm()
    return render(request, "registration/reset_password.html", {"password_reset_form": password_reset_form})


@login_required(login_url=LOGIN_URL)
def ctrl_password_change_done(request):
    user = request.user

    # Email content
    subject = "Password changed"
    from_email = email_cnf.EMAIL_HOST_USER
    to_email = [user.email]
    context = {
        "email": user.email,
        'domain': get_current_site(request),
        'site_name': 'District Coders',
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
        'year': datetime.now().year,
    }

    # Render HTML + plain fallback
    html_content = render_to_string("registration/mails/change_password_email.html", context)
    text_content = f"""
    Hello {user.username},

    Your password has been successfully changed.

    If you did not request this, please contact support.

    http://{get_current_site(request).domain}{reverse('login')}
    """

    # Send email with both versions
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

    # Render confirmation view
    template = loader.get_template('registration/change_password_done.html')
    logout(request)
    return HttpResponse(template.render({}, request))

@login_required(login_url=LOGIN_URL)
def ctrl_email_change_auth(request):
    # getting params
    new_email = request.POST.get("new_email", "")
    password = request.POST.get("password", "")
    current_user = request.user

    # conditions
    are_field_not_empty = len(new_email) > 0 and len(password) > 0
    if are_field_not_empty:
        id_password_correct = check_password(password, current_user.password)
        try:
            validate_email(new_email)
            is_form_ok = True
        except ValidationError:
            is_form_ok = False

        if UserDC.objects.filter(email=new_email).exists():
            is_form_ok = False
    else :
        id_password_correct = False
        is_form_ok = False

    if are_field_not_empty and id_password_correct and is_form_ok and current_user.email != new_email:
        # save changes
        current_user.is_active = False
        current_user.previous_email = current_user.email
        current_user.email = new_email
        current_user.save()
        send_confirm_email(request, current_user)
        # redirect
        return redirect(reverse('email_change_confirm', kwargs={"user_id": current_user.id}))
    else:
        context = {"err_msg": ""}
        if are_field_not_empty:
            if not id_password_correct:
                context["err_msg"] = error_message_cnf.PASSWORD_INVALID
            elif not is_form_ok:
                context["err_msg"] = error_message_cnf.EMAIL_INVALID

        template = loader.get_template('registration/email_change_auth.html')
        return HttpResponse(template.render(context, request))


def ctrl_login(request):
    curr_user = request.user
    if curr_user.is_authenticated:
        return redirect("/")
    return LoginView.as_view(template_name="registration/login.html")(request)

def ctrl_password_reset_done(request):
    curr_user = request.user
    if curr_user.is_authenticated:
        return redirect("/")
    return auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/reset_password_complete.html')(request)