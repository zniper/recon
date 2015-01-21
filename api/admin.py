from django.contrib import admin

import models

# Register your models here.

admin.site.register(models.CrawlRequest)
admin.site.register(models.CrawlSchedule)
admin.site.register(models.CrawlRecord)
