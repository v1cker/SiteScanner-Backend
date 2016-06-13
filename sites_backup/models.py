from __future__ import unicode_literals

from django.db import models

# Create your models here.


class SitesBackupIndex(models.Model):
    site_id = models.IntegerField(null=False)
    path = models.CharField(max_length=255, null=False)
    author = models.CharField(max_length=120, default='Anonymous')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return self.path
