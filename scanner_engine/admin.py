from django.contrib import admin
from .models import WatcherScanResult, RedirectionScanResult, ScannerLogs


class AutomaticScannerLogsAdmin(admin.ModelAdmin):
    list_display = ['id', 'addon', 'proxy', 'timestamp']


class WatcherScanResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'watcher', 'status_code', 'title', 'description', 'h1', 'timestamp']


class RedirectionScanResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'redirection', 'base_url', 'target_url', 'status_code', 'timestamp']


admin.site.register(ScannerLogs, AutomaticScannerLogsAdmin)
admin.site.register(WatcherScanResult, WatcherScanResultAdmin)
admin.site.register(RedirectionScanResult, RedirectionScanResultAdmin)
