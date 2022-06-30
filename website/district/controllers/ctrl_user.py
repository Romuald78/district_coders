import traceback

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes

from district.controllers.ctrl_main import ctrl_error
from district.models.user import UserDC
from config.constants import error_message_cnf
from toolbox.users.signup import SignupForm
from district.models.group import GroupDC
from toolbox.users.tokens import account_activation_token
from toolbox.users.update import UserUpdateForm
from toolbox.utils.user import send_confirm_email
from website import settings
from website.settings import LOGIN_URL, DEFAULT_GROUP_KEY


@login_required(login_url=LOGIN_URL)
def ctrl_user_profile(request):
    # get the user currently logged and groups that he belongs to
    curr_user = request.user
    context = {"user": curr_user}

    # Load view template
    template = loader.get_template('district/user_profile.html')

    return HttpResponse(template.render(context, request))


# No login required to sign up (indeed)
def ctrl_user_signup(request):
    form = SignupForm(request.POST, request.FILES)
    # Get default group
    groups = GroupDC.objects.filter(register_key=DEFAULT_GROUP_KEY)

    if form.is_valid() and groups.exists():
        # retrieve form data
        user = form.save()
        user.refresh_from_db()
        user.first_name = form.cleaned_data.get('first_name')
        user.last_name = form.cleaned_data.get('last_name')
        user.email = form.cleaned_data.get('email')
        user.icon = form.cleaned_data.get('icon')
        user.description = form.cleaned_data.get('description')
        user.groups.add(groups.first())
        # confirmation email
        user.is_active = False
        user.save()
        # login after signup
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password1')
        # user = authenticate(username=username, password=password)
        # login(request, user)

        return redirect(f'/accounts/confirmemail/{user.id}')
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
            return JsonResponse({"exit_code": 2, "err_msg": error_message_cnf.GROUP_REGISTER_EMPTY_KEY})

        # check if the key exists. In this case, get the id of the group concerned
        groups = GroupDC.objects.filter(register_key=register_key)
        if not groups.exists():
            return JsonResponse({"exit_code": 1, "err_msg": error_message_cnf.GROUP_REGISTER_UNVALIDE_KEY})

        if len(GroupDC.objects.filter(id=groups.first().id, userdc=user_id).all()) != 0:
            return JsonResponse({"exit_code": 9, "err_msg": error_message_cnf.GROUP_REGISTER_ALREADY_IN})

        # link the group to the user
        user_obj = UserDC.objects.get(id=user_id)
        user_obj.groups.add(groups.first())
        user_obj.save()

        # return a dictionary
        return JsonResponse({"exit_code": 0})
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
def ctrl_user_update(request):
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.icon = form.cleaned_data.get('icon')
            user.description = form.cleaned_data.get('description')
            former_email = user.email
            user.email = form.cleaned_data.get('email')
            if former_email != form.cleaned_data.get('email'):
                user.is_email_validated = False
                send_confirm_email(request, user)
            user = form.save()
            user.refresh_from_db()
            return redirect('/accounts/profile')
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
        user.is_email_validated = True
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

    if curr_user is not None and not curr_user.is_email_validated:
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

    if curr_user is not None and not curr_user.is_email_validated:
        send_confirm_email(request, curr_user)
        return JsonResponse({"exit_code": 0})
    else:
        return JsonResponse({"exit_code": 3, "err_msg": error_message_cnf.EMAIL_ALREADY_CONFIRM})


def ctrl_password_reset_request(request):
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
                        'domain': get_current_site(request),
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/accounts/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/reset_password.html",
                  context={"password_reset_form": password_reset_form})


@login_required(login_url=LOGIN_URL)
def ctrl_password_change_done(request):
    user = request.user

    # sending email
    subject = "Password changed"
    email_template_name = "registration/mails/change_password_email.html"
    c = {
        "email": user.email,
        'domain': get_current_site(request),
        'site_name': 'Website',
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    email = render_to_string(email_template_name, c)
    try:
        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

    context = {}
    # Load view template
    template = loader.get_template('registration/change_password_done.html')
    return HttpResponse(template.render(context, request))