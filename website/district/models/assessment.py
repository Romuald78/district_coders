from django.db import models

from district.models.group import GroupDC
from district.models.test import TestDC


class Assessment(models.Model):

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    training_time = models.DateTimeField()
    result_json = models.TextField(blank=True)
    groups = models.ManyToManyField(GroupDC)
    test = models.ForeignKey(TestDC, on_delete=models.CASCADE)



