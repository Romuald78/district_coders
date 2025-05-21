from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm

from district.models.assessment import Assessment
from district.models.exo2test import Exo2Test
from district.models.exotest2lang import ExoTest2Lang
from district.models.group import GroupDC
from district.models.inspector_mode import InspectorMode
from district.models.language import Language
from district.models.exercise import Exercise
from district.models.keyword import KeyWord

# Register your own models here so you can edit them
# from the Django administration web interface
from district.models.test import TestDC
from district.models.testresult import TestResult
from district.models.user import UserDC

# ----------------------------------------------
# ADMIN VALIDATORS
# ----------------------------------------------
class MyAssessmentAdminForm(ModelForm):
    def clean(self):
        # Get form data
        cleaned_data = super().clean()
        start    = cleaned_data["start_time"]
        end      = cleaned_data["end_time"]
        training = cleaned_data["training_time"]
        # First check the 3 times are in the right order
        bad_current   = False
        bad_training1 = False
        bad_training2 = False
        if start >= end:
            bad_current = True
        if training <= start:
            bad_training1 = True
        if training <= end:
            bad_training2 = True
        if bad_current or bad_training1 or bad_training2:
            msg  = 'Invalid assessment dates '
            if bad_current:
                msg += ' | start>=end'
            if bad_training1:
                msg += ' | start>=training'
            if bad_training2:
                msg += ' | end>=training'
            raise ValidationError(msg)
        # return data
        return cleaned_data


class AssessmentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ["id", "start_time", "end_time", "training_time", "result_json"]
    form = MyAssessmentAdminForm
class ExerciseAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
    list_display = ["id", "title", "description", "gen_file", "icon"]
class LanguageAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
    list_display = ["id", "name", "icon", "default_code", "language_program"]
class TestDCAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
    list_display = ["id", "title", "description", "icon"]
class InspectorModeAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
    list_display = ["id","name","icon"]
class GroupDCAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
    list_display = ["id","name","icon","register_key","description"]
class UserDCAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
    list_display = ["id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "icon", "description", "is_email_validated"]


admin.site.register(Language, LanguageAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(KeyWord)
admin.site.register(UserDC, UserDCAdmin)
admin.site.register(GroupDC, GroupDCAdmin)
admin.site.register(TestDC, TestDCAdmin)
admin.site.register(Exo2Test)
admin.site.register(ExoTest2Lang)
admin.site.register(Assessment, AssessmentAdmin)
admin.site.register(TestResult)
admin.site.register(InspectorMode, InspectorModeAdmin)


