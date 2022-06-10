from django.contrib.auth.models import AbstractUser
from django.db import models

from district.models.group import GroupDC


class UserDC(AbstractUser):

    icon = models.FileField(blank=True, upload_to="icons/users")
    description = models.TextField()
    groups = models.ManyToManyField(GroupDC)

    def __str__(self):
        out = f"[{self.id}] User {self.username}"
        return out
