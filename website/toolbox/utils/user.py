from django.http import JsonResponse

from district.models.group import GroupDC
from district.models.user import UserDC


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
