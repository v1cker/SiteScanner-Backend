from __future__ import unicode_literals

from django.apps import AppConfig


"""
This app allows to save site backup on disk.
Usualy performed after site was added.
"""
class SitesBackupConfig(AppConfig):
    name = 'sites_backup'
