"""generalnyOgarniacz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
import scanner_engine.views
import register_site.views
import user_profile.views
import manage_sites.views
from ember_api import views
import registration.backends.default.urls
from rest_framework import routers


# Rest Framework
router = routers.DefaultRouter()
router.register(r'redirections', views.ScannerEngineViewSet)
router.register(r'entriesindex-detail', views.EntriesIndexViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', scanner_engine.views.home, name='home'),

    # register_site
    url(r'^watcher_from_snapshot/$', register_site.views.site_from_snapshot_form, name='site_from_snapshot'),
    url(r'^register_watcher/$', register_site.views.register_form, name='register_site'),
    url(r'^register_redirection/$', register_site.views.register_301_form, name='register301'),
    url(r'^delete_entry/([0-9]+)/$', register_site.views.delete_entry, name='delete_site'),

    # scanner_engine
    url(r'^update/$', scanner_engine.views.update_scans, name='update_scans'),
    url(r'^update/([0-9]+)/$', scanner_engine.views.update_scans, name='update_scans'),

    # manage_sites
    url(r'^page_details/([0-9]+)/$', manage_sites.views.page_details, name='page_details'),
    url(r'^page_details/$', manage_sites.views.page_details, name='page_details'),
    url(r'^modify_site/([0-9]+)/$', manage_sites.views.modify_site, name='modify_site'),
    url(r'^modify_site/$', manage_sites.views.modify_site, name='modify_site'),

    # user_profile
    url(r'^profile/$', user_profile.views.profile, name='profile'),

    # registration
    url(r'^accounts/', include(registration.backends.default.urls)),

    # Rest framework GUI API and DOT
    url(r'^api/', include(router.urls)),
    url(r'^api/o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
