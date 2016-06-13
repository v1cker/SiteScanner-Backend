from django.contrib.auth.models import User, Group
from scanner_engine.models import RedirectionScanResult
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class RedirectionScanResultSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RedirectionScanResult
        fields = ('site_id', 'base_url', 'target_url', 'status_code', 'timestamp')
