from __future__ import unicode_literals

from django.apps import AppConfig


"""
This appp allows to register and delete entries and add-ons in the DB.
App contains models for Entry and every add-on.
"""
class RegisterSiteConfig(AppConfig):
    name = 'register_site'
