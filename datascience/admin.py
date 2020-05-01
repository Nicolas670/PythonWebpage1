from django.contrib import admin
from .models import DataUpload


class DataUploadAdmin(admin.ModelAdmin):
    list_display = ("title", "task")


admin.site.register(DataUpload)
