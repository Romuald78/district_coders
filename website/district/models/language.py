from django.db import models

# Create your own models here.
class Language(models.Model):

    name = models.CharField(max_length=32, unique=True)
    icon = models.TextField()
    default_code = models.TextField()   ## FileField ?

    def __str__(self):
        out = f"Language {self.name}"
        return out