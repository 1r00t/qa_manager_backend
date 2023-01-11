from django.contrib import admin
from . import models

admin.site.register(models.TestCase)
admin.site.register(models.Section)
admin.site.register(models.TestRun)
admin.site.register(models.TestRunCase)
