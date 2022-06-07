from django.db import models

from district.models.exercise import Exercise
from district.models.test import TestDC


class Exo2Test(models.Model):

    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    test_id = models.ForeignKey(TestDC, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        out = f"Exo2Test ex:{self.exercise_id}/test:{self.test_id}"
        return out
