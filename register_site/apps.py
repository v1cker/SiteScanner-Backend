from __future__ import unicode_literals
from django.apps import AppConfig


class RegisterSiteConfig(AppConfig):
    """
    This app allows to register and delete entries and add-ons in the DB.
    App contains models for Entry and every add-on.
    """
    name = 'register_site'
