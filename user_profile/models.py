from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UserModel(models.Model):
    user_name = models.CharField(max_length=60, blank=False, null=False)
    email = models.EmailField(max_length=60, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=False)


def __unicode(self):
    return self.user_name
