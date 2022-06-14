from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader

from district.models.group import GroupDC
from district.models.user import UserDC
from website.settings import LOGIN_URL


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


# let the user join a group
@login_required(login_url=LOGIN_URL)
def ctrl_user_register(request):
    # get parameters from request
    register_key = request.POST.get("register_key", "")
    user_id = request.POST.get("user_id", 0)

    if len(register_key) == 0 or user_id == 0:
        return JsonResponse({"exit_code": 2})

    # check if the key exists. In this case, get the id of the group concerned
    groups = GroupDC.objects.filter(register_key=register_key)
    if not groups.exists():
        return JsonResponse({"exit_code": 1})

    # link the group to the user
    user_obj = UserDC.objects.get(id=user_id)
    user_obj.groups.add(groups.first())
    user_obj.save()

    # return a dictionary
    return JsonResponse({"exit_code": 0})