from django.db import models

class TestDC(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
    icon = models.CharField(max_length=128)

    def __str__(self):
        out = f"Test '{self.title}'"
        return out