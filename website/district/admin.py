from django.contrib import admin

from district.models.assessment import Assessment
from district.models.exo2test import Exo2Test
from district.models.exotest2lang import ExoTest2Lang
from district.models.group import GroupDC
from district.models.language import Language
from district.models.exercise import Exercise
from district.models.keyword import KeyWord

# Register your own models here so you can edit them
# from the Django administration web interface
from district.models.test import TestDC
from district.models.testresult import TestResult
from district.models.user import UserDC

admin.site.register(Language)
admin.site.register(Exercise)
admin.site.register(KeyWord)
admin.site.register(UserDC)
admin.site.register(GroupDC)
admin.site.register(TestDC)
admin.site.register(Exo2Test)
admin.site.register(ExoTest2Lang)
admin.site.register(Assessment)
admin.site.register(TestResult)


