from django.db import models

class Exercise(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
    gen_file = models.CharField(unique=True, max_length=128) ## FileField ?
    icon = models.TextField()               ## FileField ?
    gen_type = models.IntegerField()

    def __str__(self):
        out = f"Exercice {self.title}"
        return out
