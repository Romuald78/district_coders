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
from toolbox.utils.route_mgr import Page

ROUTES = [
    Page('home', '', ctrl_home, log_req=False),

    Page('signup', 'accounts/signup/', ctrl_user_signup, log_req=False),
    Page('activate', 'accounts/activate/<slug:uidb64>/<slug:token>/', ctrl_user_validate_email, log_req=False),
    Page('login', 'accounts/login/', include("django.contrib.auth.urls"), log_req=False),
    Page('profile', 'accounts/profile/', ctrl_user_profile),
    Page('update', 'accounts/update/', ctrl_user_update),
    Page('group_register', 'accounts/group_register/', ctrl_json_user_register, type="json"),
    Page('my_groups', 'accounts/my_groups/', ctrl_json_user_groups, type="json"),

    Page('password_reset_request' , 'accounts/password_reset_request/', ctrl_password_reset_request, log_req=False),
    Page('password_reset_done'    , 'accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(
    template_name='registration/password_reset_done.html'), log_req=False),
    Page('password_reset_confirm' , 'accounts/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name="registration/password_reset_confirm.html"), log_req=False),
    Page('password_reset_complete','accounts/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(    template_name='registration/reset_password_complete.html'), log_req=False),

    Page('password_change_done', 'accounts/password_change/done/', ctrl_password_change_done)
    Page('password_change', 'accounts/password_change/', auth_views.PasswordChangeView.as_view(
    template_name="registration/change_password.html")),

    Page('email_change_auth', 'accounts/email_change_auth/', ctrl_email_change_auth),
    Page('email_change_confirm', 'accounts/email_change_confirm/<int:user_id>/', ctrl_email_verification, log_req=False),
    Page('email_change_send', 'accounts/email_change_send/', ctrl_json_sending_email, type="json", log_req=False),

    Page('assessment_details', 'assessment/details/<int:id_asse>/', ctrl_asse_details),
    Page('exercise_details', 'exercise/details/', ctrl_exercise_details),
    Page('exercise_write', 'exercise/write/', ctrl_exercise_write),
    Page('exercise_inspect', 'exercise/inspect/', ctrl_json_exercise_inspect, type='json'),
    Page('exercise_stats', 'exercise/stats/', ctrl_json_testresult_exists, type='json'),

]
