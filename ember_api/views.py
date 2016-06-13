from django.contrib.auth.models import User, Group
from scanner_engine.models import RedirectionScanResult
from rest_framework import viewsets
from  ember_api.serializers import UserSerializer, GroupSerializer, RedirectionScanResultSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ScannerEngineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows scanns to be bla bla bla
    """
    queryset = RedirectionScanResult.objects.all()
    serializer_class = RedirectionScanResultSerializer
