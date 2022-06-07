from django.db import models

class GroupDC(models.Model):

    name = models.CharField(max_length=128)
    icon = models.CharField(max_length=128)
    register_key = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        out = f"Group {self.name}"
        return out
