from django.db import models

from district.models.group import GroupDC
from district.models.test import TestDC


class Assessment(models.Model):

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    training_time = models.DateTimeField()
    result_json = models.TextField()
    groups = models.ManyToManyField(GroupDC)
    test_id = models.ForeignKey(TestDC, on_delete=models.CASCADE)

    def __str__(self):
        out = f"[{self.id}] Assessment test_id:{self.test_id}/start:{self.start_time}/end:{self.end_time}/train:{self.training_time}"
        return out
