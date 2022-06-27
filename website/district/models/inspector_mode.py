import os

from django.db import models

from toolbox.utils.utils import get_icon_tag, upload_imagefield_to, OverwriteStorage


class InspectorMode(models.Model):

    name = models.CharField(max_length=64, unique=True)
    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to=upload_imagefield_to, storage=OverwriteStorage)

    def get_upload_to_path(self):
        return os.path.join("icons","modes")

    # Display of the icon in the admin interface
    def image_tag(self):
        return get_icon_tag(self.icon)

    image_tag.short_description = 'icon picture'
    image_tag.allow_tags = True

    def __str__(self):
        out = f"[{self.id}] InspectorMode {self.name}"
        return out
