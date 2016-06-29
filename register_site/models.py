from __future__ import unicode_literals
from django.db import models


# New models 09.06.16
class EntriesIndex(models.Model):
    alias = models.CharField(max_length=255, blank=True, null=False)
    owner_username = models.CharField(max_length=255, blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    watcher_exists = models.BooleanField(default=0)
    redirections_exists = models.BooleanField(default=0)
    archive_exists = models.BooleanField(default=0)

    def __unicode__(self):
        return self.alias

    def has_watcher(self):
        return bool(self.watcher_exists)

    def has_redirections(self):
        return bool(self.redirections_exists)

    def has_archive(self):
        return bool (self.archive_exists)


class WatchersIndex(models.Model):
    entry = models.ForeignKey(EntriesIndex, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    h1 = models.CharField(max_length=255, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_scan_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class RedirectionsIndex(models.Model):
    entry = models.ForeignKey(EntriesIndex, on_delete=models.CASCADE)
    base_url = models.CharField(max_length=255, blank=False, null=False)
    target_url = models.CharField(max_length=255, blank=False, null=False)
    status_code = models.IntegerField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_scan_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.base_url


class ArchivesIndex(models.Model):
    entry = models.ForeignKey(EntriesIndex, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=False, null=False)
    interval_in_days = models.IntegerField(blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    last_copy_id = models.IntegerField(null=True, blank=True)
