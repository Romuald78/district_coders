from datetime import timedelta

from django.db import models

from district.models.assessment import Assessment
from district.models.exotest2lang import ExoTest2Lang
from district.models.user import UserDC


class TestResult(models.Model):

    exo_test2lang_id = models.ForeignKey(ExoTest2Lang, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserDC, on_delete=models.CASCADE)
    nb_test_try = models.IntegerField(default=0)
    solve_time = models.DurationField(default=timedelta())
    solve_code = models.TextField()
    solve_percentage = models.FloatField(default=0)
    assessment_id = models.ForeignKey(Assessment, on_delete=models.CASCADE)

    def __str__(self):
        out = f"TestResult exo_test2lang_id:{self.exo_test2lang_id}/user:{self.user_id}"
        return out
