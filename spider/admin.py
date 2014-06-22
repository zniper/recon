from django.contrib import admin

from spider import models

admin.site.register(models.Resource)
admin.site.register(models.ItemRule)
admin.site.register(models.Item)
admin.site.register(models.LocalItem)
