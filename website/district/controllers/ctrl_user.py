from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from toolbox.users.signup import SignupForm
from district.models.group import GroupDC
from toolbox.users.update import UserUpdateForm
from website.settings import LOGIN_URL, DEFAULT_GROUP_KEY


@login_required(login_url=LOGIN_URL)
def ctrl_user_profile(request):
    # get the current user currently logged and groups that he belongs to
    curr_user = request.user
    context = {"user": curr_user}

    all_groups = GroupDC.objects.filter(userdc=curr_user)

    groups_users = {}
    for g in all_groups:
        user_name = [user.username for user in g.userdc_set.all()]
        if g.id not in groups_users:
            groups_users[g.id] = {"group_obj": g,
                                  "group_users": user_name}
        else:
            groups_users[g.id]["group_users"] += user_name

    context["groups"] = groups_users

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
        user.save()
        # login after signup
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        form = SignupForm()

    context = {'form':form}
    # Load view template
    template = loader.get_template('registration/signup.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url=LOGIN_URL)
def ctrl_user_update(request):
    user = request.user

    if request.method == "POST":
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.icon = form.cleaned_data.get('icon')
            user.description = form.cleaned_data.get('description')
            user = form.save()
            user.refresh_from_db()
            return redirect('/accounts/profile')
    else:
        form = UserUpdateForm(instance=user)

    context = {'form':form}
    # Load view template
    template = loader.get_template('registration/update.html')
    return HttpResponse(template.render(context, request))
