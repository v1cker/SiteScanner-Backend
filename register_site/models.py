from __future__ import unicode_literals
from django.db import models


# New models 09.06.16
class EntriesIndex(models.Model):
    alias = models.CharField(max_length=255, blank=True, null=False)
    owner_username = models.CharField(max_length=255, blank=False, null=False, verbose_name='Owner')
    url = models.URLField(max_length=255, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    watcher_exists = models.BooleanField(default=0)
    redirections_exists = models.BooleanField(default=0)

    def __unicode__(self):
        return self.alias

    def has_watcher(self):
        return bool(self.watcher_exists)

    def has_redirections(self):
        return bool(self.redirections_exists)

    class JSONAPIMeta:
        resource_name = "entry"


class WatchersIndex(models.Model):
    entry = models.ForeignKey(EntriesIndex, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name='Title')
    description = models.TextField(blank=False, null=False, verbose_name='Description')
    h1 = models.CharField(max_length=255, blank=False, null=False, verbose_name='H1 header')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_scan_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class RedirectionsIndex(models.Model):
    entry = models.ForeignKey(EntriesIndex, on_delete=models.CASCADE)
    scan = models.ForeignKey('scanner_engine.RedirectionScanResult', default=None, null=True, related_name='redirections_scan')
    base_url = models.URLField(max_length=255, blank=False, null=False, verbose_name='Base url')
    target_url = models.URLField(max_length=255, blank=False, null=False, verbose_name='Target url')
    status_code = models.IntegerField(blank=False, null=False, verbose_name='Response code')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.base_url

    class JSONAPIMeta:
        resource_name = "redirection"
