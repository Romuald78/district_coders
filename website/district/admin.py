from django.contrib import admin
from district.models.models import Language, Exercice, KeyWord

# Register your own models here so you can edit them
# from the Django administration web interface
admin.site.register(Language)
admin.site.register(Exercice)
admin.site.register(KeyWord)

