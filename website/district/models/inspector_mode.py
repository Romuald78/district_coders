from django.db import models


class InspectorMode(models.Model):

    name = models.CharField(max_length=64, unique=True)
    icon = models.FileField(blank=True, upload_to="icons/modes")

    def __str__(self):
        out = f"[{self.id}] InspectorMode {self.name}"
        return out
