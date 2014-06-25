from django.contrib import admin

from spider import models

admin.site.register(models.Resource)
admin.site.register(models.LocalContent)
admin.site.register(models.WordSet)
