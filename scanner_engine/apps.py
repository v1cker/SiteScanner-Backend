from __future__ import unicode_literals

from django.apps import AppConfig


"""
App crawls sites registered in the DB and saves the results.
It also contains task for scheduled scans.
"""
class ScannerEngineConfig(AppConfig):
    name = 'scanner_engine'
