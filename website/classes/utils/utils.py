import os

from django.utils.safestring import mark_safe

from website.settings import MEDIA_URL


def getIconTag(icon_url):
    icon_path = os.path.join(MEDIA_URL, f"{icon_url}")
    out = "<img src=\""
    out += f"{icon_path}"
    out += "\" height=\"48\" />"
    return mark_safe(out)
