import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from toolbox.utils.utils import get_icon_tag, recreate_dir
from district.models.group import GroupDC
from website.settings import MEDIA_ROOT


def user_icon_upload_to(instance, filename):
    print("filename", filename)
    usrnam = instance.username
    basedir = os.path.join('icons', 'users', usrnam)
    recreate_dir(os.path.join(MEDIA_ROOT, basedir), clear=False)
    # we do not use the original filename but username instead
    filename = f"{usrnam}_icon.png"
    relative_path = os.path.join(basedir, filename)
    full_path = os.path.join(MEDIA_ROOT, relative_path)
    # remove existing icon file if needed
    if os.path.isfile(full_path):
        os.remove(full_path)
    # return full icon path
    return relative_path

class UserDC(AbstractUser):

    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to=user_icon_upload_to)
    description = models.TextField(blank=True)
    groups = models.ManyToManyField(GroupDC)
    is_email_validated = models.BooleanField(default=False)

    # Display of the icon in the admin interface
    def image_tag(self):
        return get_icon_tag(self.icon)

    image_tag.short_description = 'user picture'
    image_tag.allow_tags = True

    def __str__(self):
        out = f"[{self.id}] User {self.username}"
        return out
