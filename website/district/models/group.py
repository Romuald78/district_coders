from django.db import models

from toolbox.utils.utils import get_icon_tag


class GroupDC(models.Model):

    name = models.CharField(max_length=128)
    # TODO : add width and height values to ImageField ?
    icon = models.ImageField(blank=True, upload_to="icons/groups")
    register_key = models.CharField(max_length=32)
    description = models.TextField(blank=True)

    # Display of the icon in the admin interface
    def image_tag(self):
        return get_icon_tag(self.icon)

    image_tag.short_description = 'group picture'
    image_tag.allow_tags = True

    def __str__(self):
        out = f"[{self.id}] Group {self.name}"
        return out
