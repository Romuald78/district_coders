from django.contrib.auth.models import AbstractUser
from django.db import models

from district.models.group import GroupDC


class UserDC(AbstractUser):

    icon = models.CharField(max_length=128)
    description = models.TextField()
    groups = models.ManyToManyField(GroupDC)

    def __str__(self):
        out = f"User {self.username}"
        return out
