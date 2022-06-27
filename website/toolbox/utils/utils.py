import os
from shutil import rmtree

from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe

from website.settings import MEDIA_URL, MEDIA_ROOT


def recreate_dir(dirname, clear=True):
    # if directory exists, remove it if needed
    if os.path.exists(dirname):
        if clear:
            rmtree(dirname)
    else:
        clear = True
    # create directory if needed
    if clear:
        os.makedirs(dirname)


def get_icon_tag(icon_url):
    icon_path = os.path.join(MEDIA_URL, f"{icon_url}")
    out = "<img src=\""
    out += f"{icon_path}"
    out += "\" height=\"48\" />"
    return mark_safe(out)


# Remove same file if it exists (used to overwrite)
class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=128):
        full_path = os.path.join(MEDIA_ROOT, name)
        # If the filename already exists, remove it as if it was a true file system
        if os.path.exists(full_path):
            # os.close()
            try:
                os.remove(full_path)
            except Exception as e:
                print(e)
                return ""
        return name


def upload_imagefield_to(instance, filename):
    path = instance.get_upload_to_path()
    rel_path = os.path.join(path, filename)
    return rel_path
