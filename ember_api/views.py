from register_site.models import RedirectionsIndex, EntriesIndex
from rest_framework import viewsets
from ember_api.serializers import RedirectionSerializer, EntriesIndexSerializer


class ScannerEngineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view and edit redirections
    """
    resource_name = 'Redirection'
    queryset = RedirectionsIndex.objects.all()
    serializer_class = RedirectionSerializer


class EntriesIndexViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view and edit entries
    """
    resource_name = 'Entry'
    queryset = EntriesIndex.objects.all()
    serializer_class = EntriesIndexSerializer
