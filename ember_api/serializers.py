from register_site.models import RedirectionsIndex, EntriesIndex
from scanner_engine.models import RedirectionScanResult
from rest_framework import serializers


class EntriesIndexSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EntriesIndex
        fields = ('alias', 'owner_username', 'url', 'timestamp',
                  'watcher_exists', 'redirections_exists')


class RedirectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RedirectionsIndex
        fields = ('entry', 'base_url', 'target_url', 'status_code', 'timestamp', 'updated', 'scan')


class RedirectionScanResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RedirectionScanResult
        fields = ('base_url', 'status_code', 'target_url', 'timestamp')