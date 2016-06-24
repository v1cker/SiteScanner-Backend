from __future__ import unicode_literals
from django.db import models
from register_site.models import WatchersIndex, RedirectionsIndex, EntriesIndex


"""
Log produced with every scan.
"""
class ScannerLogs(models.Model):
    ADDON_TYPES = (
        (WatchersIndex, 'Watcher'),
        (RedirectionsIndex, 'Redirection')
    )
    addon = models.CharField(max_length=120, null=True, choices=ADDON_TYPES)
    proxy = models.CharField(max_length=120, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


"""
Model for result of single scan of the Watcher.
"""
class WatcherScanResult(models.Model):
    watcher = models.ForeignKey(WatchersIndex)
    status_code = models.SmallIntegerField(blank=False, null=True)
    title = models.CharField(max_length=120, blank=False, null=True)
    description = models.CharField(max_length=240,  blank=False, null=True)
    h1 = models.CharField(max_length=240, blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return str(self.title)


"""
Model for result of single scan of Redirection.
"""
class RedirectionScanResult(models.Model):
    redirection = models.ForeignKey(RedirectionsIndex)
    base_url = models.URLField(max_length=60, blank=False, null=False)
    target_url = models.URLField(max_length=60, blank=False, null=False)
    status_code = models.SmallIntegerField(blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return str(self.base_url)
