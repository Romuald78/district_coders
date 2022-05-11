from django.db import models

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=32)
    icon = models.Field