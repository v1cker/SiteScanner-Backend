from __future__ import unicode_literals
from django.db import models


"""
The most basic model of the entire application.
Entry represents one specific domain to be observed.
Entry can be associated with many diferent add-ons
Details on add-ons below.
"""
class EntriesIndex(models.Model):
    alias = models.CharField(max_length=255, blank=True, null=False)
    owner_username = models.CharField(max_length=255, blank=False, null=False)
    url = models.CharField(max_length=255, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    # Add-ons
    watcher_exists = models.BooleanField(default=0)
    redirections_exists = models.BooleanField(default=0)

    def __unicode__(self):
        return self.alias

    def has_watcher(self):
        return bool(self.watcher_exists)

    def has_redirections(self):
        return bool(self.redirections_exists)


"""
Add-on.
Every Entry can have only one Watcher.
Watcher keeps track of meta title, meta description and first H1 of the site.
"""
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


"""
Add-on.
Every entry can have multiple Redirections.
Redirection add-on checks if base url redirects to target url.
Target url should be the same as url of the associated Entry,
although it don't has to be. 
"""
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
