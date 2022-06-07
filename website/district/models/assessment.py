from django.db import models

from district.models.group import GroupDC


class Assessment(models.Model):

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    training_time = models.DateTimeField()
    result_json = models.TextField()
    groups = models.ForeignKey(GroupDC, on_delete=models.CASCADE)

    def __str__(self):
        out = f"Group {self.name}"
        return out
