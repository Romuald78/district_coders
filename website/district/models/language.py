import os

from django.db import models


# Create your own models here.
from toolbox.utils.utils import get_icon_tag, upload_imagefield_to, OverwriteStorage


class Language(models.Model):
    name = models.CharField(max_length=32, unique=True)
    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to=upload_imagefield_to) #, storage=OverwriteStorage)
    default_code = models.TextField(blank=True)
    language_program = models.CharField(max_length=32, unique=True, default="None")

    def get_upload_to_path(self):
        return os.path.join("icons","languages")

    # Display of the icon in the admin interface
    def image_tag(self):
        return get_icon_tag(self.icon)

    image_tag.short_description = 'icon picture'
    image_tag.allow_tags = True


    def __str__(self):
        out = f"[{self.id}] Language: {self.name}"
        return out