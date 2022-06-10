from django.contrib import admin
from django.db import models


# Create your own models here.
from classes.utils.utils import getIconTag


class Language(models.Model):
    name = models.CharField(max_length=32, unique=True)
    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to="icons/languages")
    default_code = models.TextField()   ## FileField ?
    language_program = models.CharField(max_length=64, unique=True, default="")

    # Display of the icon in the admin interface
    def image_tag(self):
        return getIconTag(self.icon)

    image_tag.short_description = 'icon picture'
    image_tag.allow_tags = True


    def __str__(self):
        out = f"[{self.id}] Language: {self.name}"
        return out