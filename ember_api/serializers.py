from register_site.models import RedirectionsIndex, EntriesIndex
from rest_framework import serializers


class EntriesIndexSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EntriesIndex
        fields = ('alias', 'owner_username', 'url', 'timestamp',
                  'watcher_exists', 'redirections_exists')


class RedirectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RedirectionsIndex
        fields = ('entry', 'base_url', 'target_url', 'status_code', 'timestamp', 'updated', 'last_scan_id')
