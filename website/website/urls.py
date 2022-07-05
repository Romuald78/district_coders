"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from district.controllers.ctrl_exercise import ctrl_exercise_write, ctrl_json_exercise_inspect, ctrl_exercise_details
from district.controllers.ctrl_testresult import ctrl_json_testresult_exists
from district.controllers.ctrl_user import ctrl_user_profile, ctrl_user_signup, ctrl_json_user_register, \
    ctrl_json_user_groups, ctrl_user_update, ctrl_user_validate_email, ctrl_email_verification, \
    ctrl_json_sending_email, ctrl_password_reset_request, ctrl_password_change_done, ctrl_email_change_auth
from district.controllers.ctrl_main import ctrl_home
from district.controllers.ctrl_assessment import ctrl_asse_details
from website import settings

urlpatterns = [
    # [VIEW] Documentation Generation (before 'admin' URL in order to avoid interceptions)
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    # [VIEW] Administration View
    path('admin/'    , admin.site.urls),

    # [VIEW] Reset password
    path('accounts/password_reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name='registration/reset_password_done.html'),name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/reset_password_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/reset_password_complete.html'), name='password_reset_complete'),
    path("accounts/password_reset/", ctrl_password_reset_request, name="password_reset"),
    # [VIEW] Change password
    path("accounts/password_change/done/", ctrl_password_change_done, name="password_change_done"),
    path("accounts/password_change/", auth_views.PasswordChangeView.as_view(
        template_name="registration/change_password.html"), name="password_change"),
    # [VIEW] Change email
    path("accounts/email_change_auth/", ctrl_email_change_auth),
    # [VIEW] Authent views
    path("accounts/", include("django.contrib.auth.urls")),
    # [VIEW] Let a user join a group
    path('accounts/signup/', ctrl_user_signup),
    # [VIEW] the email sending confirmation page
    path('accounts/confirmemail/<int:user_id>/', ctrl_email_verification),
    # [VIEW] Validate the email address
    path('accounts/activate/<slug:uidb64>/<slug:token>/', ctrl_user_validate_email, name="ctrl_user_validate_email"),
    # [VIEW] The user profile View
    path('accounts/profile/', ctrl_user_profile),
    # [VIEW] Let a user update information
    path('accounts/update/', ctrl_user_update),
    # [JSON] Let a user join a group
    path('accounts/register/', ctrl_json_user_register),
    # [JSON] Fetch all user's groups
    path('accounts/mygroups/', ctrl_json_user_groups),
    # [JSON] Sending email to confirm
    path('accounts/sendemailconfirmation/', ctrl_json_sending_email),

    # [VIEW] The list of exercises of an assessment View
    path('assessment/details/<int:id_asse>', ctrl_asse_details, name="assessment_details"),

    # [VIEW] The wording(without code editor) of an exercise
    path('exercise/details/', ctrl_exercise_details, name="exercise_details"),
    # [VIEW] The training exercise View (with code editor)
    path('exercise/write/', ctrl_exercise_write, name="exercise_write"),
    # [JSON] Verify an exercise
    path('exercise/inspect/', ctrl_json_exercise_inspect),
    # [JSON] Verify the existence of a TestResult
    path('exercise/createstat/', ctrl_json_testresult_exists),

    # [VIEW] HOME
    path('', ctrl_home),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
