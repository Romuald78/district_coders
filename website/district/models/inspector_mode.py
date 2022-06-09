from django.db import models


class InspectorMode(models.Model):

    name = models.CharField(max_length=64)
    icon = models.CharField(max_length=128, default="")

    def __str__(self):
        out = f"[{self.id}] InspectorMode {self.name}"
        return out
