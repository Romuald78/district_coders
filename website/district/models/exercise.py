from django.db import models

from district.models.inspector_mode import InspectorMode


class Exercise(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
    gen_file = models.CharField(unique=True, max_length=128) ## FileField ?
    icon = models.TextField()               ## FileField ?
    gen_type_id = models.ForeignKey(InspectorMode, on_delete=models.CASCADE)

    def __str__(self):
        out = f"[{self.id}] Exercice {self.title}"
        return out
