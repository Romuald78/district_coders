from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm
# from setuptools._entry_points import _

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
        # Get all assessments
        assess = Assessment.objects.all()
        # Get current object id and remove it from the list if needed
        assess_id = self.instance.pk
        if assess_id is not None:
            assess = assess.filter(~Q(id=assess_id))
        # Now compare the current form times with all
        # the other assessment times
        # We only need to check the [start-end] ranges
        # do not overlap
        for a in assess:
            s1 = start
            e1 = end
            s2 = a.start_time
            e2 = a.end_time
            if e1 > s2 and s1 < e2:
                # collision : we can raise an error
                msg  = 'Assessment range OVERLAP with '
                msg += f"id={a.id}"
                raise ValidationError(msg)
        # return data
        return cleaned_data


class AssessmentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    form = MyAssessmentAdminForm
class ExerciseAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
class LanguageAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
class TestDCAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
class InspectorModeAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
class GroupDCAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)
class UserDCAdmin(admin.ModelAdmin):
    readonly_fields = ('id','image_tag',)

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


