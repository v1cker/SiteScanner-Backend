from django.contrib import admin
from .forms import EntriesIndexForm, WatchersIndexForm, RedirectionsIndexForm
from .models import WatchersIndex, EntriesIndex, RedirectionsIndex, ArchivesIndex


class EntriesIndexAdmin(admin.ModelAdmin):
    list_display = ['id', 'alias', 'owner_username', 'url', 'timestamp', 'watcher_exists', 'redirections_exists',
                    'archive_exists']
    form = EntriesIndexForm


class WatchersIndexAdmin(admin.ModelAdmin):
    list_display = ['id', 'entry', 'title', 'description', 'h1', 'timestamp', 'updated', 'last_scan_id']
    form = WatchersIndexForm


class RedirectionsIndexAdmin(admin.ModelAdmin):
    list_display = ['id', 'entry', 'base_url', 'target_url', 'status_code', 'timestamp', 'updated', 'last_scan_id']
    form = RedirectionsIndexForm


class ArchivesIndexAdmin(admin.ModelAdmin):
    pass

admin.site.register(EntriesIndex, EntriesIndexAdmin)
admin.site.register(WatchersIndex, WatchersIndexAdmin)
admin.site.register(RedirectionsIndex, RedirectionsIndexAdmin)
admin.site.register(ArchivesIndex, ArchivesIndexAdmin)
