from django.db import models

# Create your models here.
class Language(models.Model):

    name = models.CharField(max_length=32, unique=True)
    icon = models.TextField()
    default_code = models.TextField()

    def __str__(self):
        out  = "{\n"
        out += f"\"name\":\"{self.name}\",\n"
        out += f"\"icon\":\"{self.icon}\",\n"
        out += f"\"default_code\":\"{self.default_code.encode()}\"\n"
        out += "}"
        return out