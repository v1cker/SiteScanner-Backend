from django.contrib import admin
from .models import WatcherScanResult, RedirectionScanResult, ArchiveLocalCopy, ScannerLogs


class AutomaticScannerLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'addon', 'proxy', 'message','timestamp']


class WatcherScanResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'watcher', 'status_code', 'title', 'description', 'h1', 'timestamp']


class RedirectionScanResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'redirection', 'base_url', 'target_url', 'status_code', 'timestamp']


class ArchiveLocalCopyAdmin(admin.ModelAdmin):
    pass


admin.site.register(ScannerLogs, AutomaticScannerLogsAdmin)
admin.site.register(WatcherScanResult, WatcherScanResultAdmin)
admin.site.register(RedirectionScanResult, RedirectionScanResultAdmin)
admin.site.register(ArchiveLocalCopy, ArchiveLocalCopyAdmin)
