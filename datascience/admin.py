from django.contrib import admin
from .models import DataUpload, TextUpload


class DataUploadAdmin(admin.ModelAdmin):
    list_display = ("title", "task")


class TextUploadAdmin(admin.ModelAdmin):
    list_display = ("title", "task")


admin.site.register(DataUpload)
admin.site.register(TextUpload)