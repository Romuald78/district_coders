import os

from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe

from website.settings import MEDIA_URL, MEDIA_ROOT


def getIconTag(icon_url):
    icon_path = os.path.join(MEDIA_URL, f"{icon_url}")
    out = "<img src=\""
    out += f"{icon_path}"
    out += "\" height=\"48\" />"
    return mark_safe(out)


# Remove same file if it exists (used to overwrite)
class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length):
        full_path = os.path.join(MEDIA_ROOT, name)
        # If the filename already exists, remove it as if it was a true file system
        if os.path.exists(full_path):
            os.remove(full_path)
        return name

def upload_imagefield_to(instance, filename):
    path = instance.get_upload_to_path()
    rel_path = os.path.join(path, filename)
    return rel_path
