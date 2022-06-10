from django.db import models

from classes.utils.utils import getIconTag


class GroupDC(models.Model):

    name = models.CharField(max_length=128)
    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to="icons/groups")
    register_key = models.CharField(max_length=128)
    description = models.TextField()

    # Display of the icon in the admin interface
    def image_tag(self):
        return getIconTag(self.icon)

    image_tag.short_description = 'icon picture'
    image_tag.allow_tags = True


def __str__(self):
        out = f"Group {self.name}"
        return out
