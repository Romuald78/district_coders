import os

from django.db import models

from classes.utils.utils import getIconTag, upload_imagefield_to


class InspectorMode(models.Model):

    name = models.CharField(max_length=64, unique=True)
    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to=upload_imagefield_to)

    def get_upload_to_path(self):
        return os.path.join("icons","modes")

    # Display of the icon in the admin interface
    def image_tag(self):
        return getIconTag(self.icon)

    image_tag.short_description = 'icon picture'
    image_tag.allow_tags = True

    def __str__(self):
        out = f"[{self.id}] InspectorMode {self.name}"
        return out
