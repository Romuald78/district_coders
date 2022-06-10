from django.contrib import admin

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
admin.site.register(Assessment)
admin.site.register(TestResult)
admin.site.register(InspectorMode, InspectorModeAdmin)


