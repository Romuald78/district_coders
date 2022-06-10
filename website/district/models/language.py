from django.contrib import admin
from django.db import models


# Create your own models here.
class Language(models.Model):
    name = models.CharField(max_length=32, unique=True)
    icon = models.FileField(blank=True, upload_to="icons/languages")
    default_code = models.TextField()   ## FileField ?
    language_program = models.CharField(max_length=64, unique=True, default="")

    def __str__(self):
        out = f"[{self.id}] Language: {self.name}"
        return out