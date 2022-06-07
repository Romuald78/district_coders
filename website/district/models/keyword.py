from django.db import models

from district.models.exercise import Exercise


class KeyWord(models.Model):

    word = models.CharField(max_length=64)
    exercices = models.ManyToManyField(Exercise)

    def __str__(self):
        out = f"Word '{self.word}'"
        return out
