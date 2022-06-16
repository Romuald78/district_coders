import os
import urllib.parse

from django.db import models
from django.utils.html import escape
from django.utils.safestring import mark_safe

from toolbox.utils.utils import getIconTag
from district.models.inspector_mode import InspectorMode
from website.settings import MEDIA_URL


class Exercise(models.Model):

    title = models.CharField(max_length=128)
    description = models.TextField()
    gen_file = models.CharField(unique=True, max_length=128) ## FileField ? No because here we only use the name (and not the extension)
    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to="icons/exercises")               ## FileField ?
    insp_mode_id = models.ForeignKey(InspectorMode, on_delete=models.CASCADE)

    # Display of the icon in the admin interface
    def image_tag(self):
        return getIconTag(self.icon)

    image_tag.short_description = 'icon picture'
    image_tag.allow_tags = True

    def __str__(self):
        out  = f"[{self.id}] Exercise {self.title}"
        return out

