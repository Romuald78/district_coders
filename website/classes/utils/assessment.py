from django.contrib.auth.decorators import login_required
from django.utils import timezone

from district.models.assessment import Assessment
from website.settings import LOGIN_URL



# retrieve all the current assessments
def ctrl_current_asse(request):
    # get current user
    curr_user = request.user

    # get current assessment
    in_progress = Assessment.objects.filter(
        start_time__lte=timezone.now(),
        end_time__gt=timezone.now(),
        groups__userdc=curr_user)

    return in_progress



# retrieve all the past assessments
def ctrl_past_asse(request):
    # get current user
    curr_user = request.user

    training = Assessment.objects.filter(
        start_time__lt=timezone.now(),
        end_time__lte=timezone.now(),
        training_time__lte=timezone.now(),
        groups__userdc=curr_user)

    return training

# retrieve all the future assessments
def ctrl_future_asse(request):
    # get current user
    curr_user = request.user

    future = Assessment.objects.filter(
        start_time__gt=timezone.now(),
        end_time__gt=timezone.now(),
        groups__userdc=curr_user)

    return future