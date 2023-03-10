from django.contrib import admin
from . import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "full_section_hierachy")


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("case_id", "section", "title")


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.TestCase, TestCaseAdmin)
admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.TestRun)
admin.site.register(models.TestResult)
