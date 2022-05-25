from django.db import models

# Create your own models here.
class Language(models.Model):

    name = models.CharField(max_length=32, unique=True)
    icon = models.TextField()
    default_code = models.TextField()   ## FileField ?

    def __str__(self):
        out = f"Language {self.name}"
        return out


class Exercice(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField()
    genFile = models.TextField(unique=True) ## FileField ?
    icon = models.TextField()               ## FileField ?

    def __str__(self):
        out = f"Exercice {self.title}"
        return out


class KeyWord(models.Model):

    word = models.CharField(max_length=64)
    exercices = models.ManyToManyField(Exercice)

    def __str__(self):
        out = f"Word '{self.word}'"
        return out
