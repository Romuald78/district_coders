from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from toolbox.utils.utils import getIconTag
from district.models.group import GroupDC


class UserDC(AbstractUser):

    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to="icons/users")
    description = models.TextField(blank=True)
    groups = models.ManyToManyField(GroupDC)

    # Display of the icon in the admin interface
    def image_tag(self):
        return getIconTag(self.icon)

    image_tag.short_description = 'icon picture'
    image_tag.allow_tags = True

    def __str__(self):
        out = f"[{self.id}] User {self.username}"
        return out
