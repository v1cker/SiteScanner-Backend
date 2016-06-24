from __future__ import unicode_literals

from django.db import models
from register_site.models import EntriesIndex


"""
Logs of every performed site backup
"""
class SitesBackupIndex(models.Model):
    entry = models.ForeignKey(EntriesIndex)
    path = models.CharField(max_length=255, null=False)
    author = models.CharField(max_length=120, default='Anonymous')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return str(self.id)
