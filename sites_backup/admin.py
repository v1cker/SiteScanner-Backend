from django.contrib import admin

from .models import SitesBackupIndex

# Register your models here.


class SitesBackupIndexAdmin(admin.ModelAdmin):
    list_display = ['id', 'site_id', 'path', 'author', 'timestamp']


admin.site.register(SitesBackupIndex, SitesBackupIndexAdmin)
