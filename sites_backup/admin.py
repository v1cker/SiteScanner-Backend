from django.contrib import admin
from .models import SitesBackupIndex


class SitesBackupIndexAdmin(admin.ModelAdmin):
    list_display = ['id', 'entry', 'path', 'author', 'timestamp']


admin.site.register(SitesBackupIndex, SitesBackupIndexAdmin)
