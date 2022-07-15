from django.db import models

from district.models.exercise import Exercise
from district.models.test import TestDC


class Exo2Test(models.Model):

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    test = models.ForeignKey(TestDC, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    solve_percentage_req = models.FloatField(default=100.0) # TODO par défaut on bloque l'accès aux exos suivant (valeur 100%)

    def __str__(self):
        out = f"Exo2Test {self.id} ex:{self.exercise}/test:{self.test}"
        return out
