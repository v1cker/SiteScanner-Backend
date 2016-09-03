from scanner_engine.utils.redirection.utils import run_redirection_scan
from scanner_engine.utils.watcher.utils import run_watcher_scan
from register_site.models import RedirectionsIndex, EntriesIndex, WatchersIndex
from scanner_engine.models import RedirectionScanResult
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ember_api.serializers import RedirectionSerializer, EntriesIndexSerializer, RedirectionScanResultSerializer
from register_site.utils import parse_domain_name

from django.contrib import admin
admin.autodiscover()
from rest_framework import permissions, routers, serializers, viewsets
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.decorators import protected_resource


class ScannerEngineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view redirections
    """
    permission_classes = [permissions.IsAuthenticated]
    resource_name = 'redirection'
    serializer_class = RedirectionSerializer
    queryset = RedirectionsIndex.objects.all()

    def get_queryset(self):
        user = self.request.user
        return RedirectionsIndex.objects.filter(entry__owner_username=user.username)


class EntriesIndexViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view entries
    """
    permission_classes = [permissions.IsAuthenticated]
    resource_name = 'entry'
    queryset = EntriesIndex.objects.all()
    serializer_class = EntriesIndexSerializer

    def get_queryset(self):
        user = self.request.user
        return EntriesIndex.objects.filter(owner_username=user.username)


class RedirectionScanViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to view redirection scans
    """
    permission_classes = [permissions.IsAuthenticated]
    resource_name = 'redirection-scan'
    queryset = RedirectionScanResult.objects.all()
    serializer_class = RedirectionScanResultSerializer

    def get_queryset(self):
        user = self.request.user
        return RedirectionScanResult.objects.filter(redirection__entry__owner_username=user.username)


@api_view(['POST'])
@protected_resource()
def UpdateScan(request):
    """
    API endpoint that allows to update entry with given id
    Function reponses with json
    """
    entry_id = None
    is_success = True
    message = ''

    if 'id' in request.POST:
        entry_id = request.POST['id']
        entry = EntriesIndex.objects.get(id=entry_id)
        if entry.has_watcher():
            if len(WatchersIndex.objects.filter(entry=entry)) == 1:
                run_watcher_scan(WatchersIndex.objects.get(entry=entry))
            else:
                is_success = False
                message = 'Watcher scan error!'
                return Response({
                    'success': is_success,
                    'error': not is_success,
                    'message': message,
                    'id': entry_id
                })
        if entry.has_redirections():
            if len(RedirectionsIndex.objects.filter(entry=entry)) != 0:
                for redirection in RedirectionsIndex.objects.filter(entry=entry):
                    run_redirection_scan(redirection, number_of_proxies_to_use=1)
            else:
                entry.redirections_exists = 0
                entry.save()
                is_success = False
                message = 'Redirection scan error!'
                return Response({
                    'success': is_success,
                    'error': not is_success,
                    'message': message,
                    'id': entry_id
                })
        message = 'Entry with id ' + entry_id + ' updated!'
    else:
        is_success = False
        message = 'Entry id not given!'

    return Response({
        'success': is_success,
        'error': not is_success,
        'message': message,
        'id': entry_id
    })


@api_view(['POST'])
@protected_resource()  # TODO delete only your own entries
def delete_entry(request):
    """
    API endpoint that allows to delete entry with given id
    Function reponses with json
    """
    entry_id = None
    is_success = True
    message = ''

    if 'id' in request.POST:
        entry_id = request.POST['id']
        if len(EntriesIndex.objects.filter(id=entry_id)) > 0:
            entry = EntriesIndex.objects.get(id=entry_id)
            entry.delete()
            message = 'Entry has been deleted.'
        else:
            is_success = False
            message = 'Entry with given id not found.'
            return Response({
                'success': is_success,
                'error': not is_success,
                'message': message,
                'id': entry_id
            })
    else:
        is_success = False
        message = 'Entry id not given!'

    return Response({
        'success': is_success,
        'error': not is_success,
        'message': message,
        'id': entry_id
    })


@api_view(['POST'])
@protected_resource()
def register_redirection(request):
    """
    API endpoint that allows to add new redirection to database
    Function reponses with json
    """
    alias = None
    base_url = None
    target_url = None
    redirection_code = None
    is_success = True
    message = ''

    if 'base_url' in request.POST and 'target_url' in request.POST:
        new_entry = EntriesIndex()
        new_entry.url = request.POST['base_url']
        new_entry.owner_username = request.user.username
        if not 'alias' in request.POST:
            new_entry.alias = parse_domain_name(new_entry.url)
        else:
            new_entry.alias = request.POST['alias']
        new_entry.save()
        new_redirection = RedirectionsIndex()
        new_redirection.entry = new_entry
        if 'code' in request.POST:
            new_redirection.status_code = request.POST['code']
        else:
            new_redirection.status_code = 301
        new_redirection.base_url = new_entry.url
        new_redirection.target_url = request.POST['target_url']
        new_redirection.save()
        new_entry.redirections_exists = 1
        new_entry.save()
        """
        Scan newly added entry, to have a least one scan in the DB.
        It is necessary to display templates correctly.
        """
        run_redirection_scan(new_redirection, number_of_proxies_to_use=1)
        message = 'Redirection registered.'
    else:
        is_success = False
        message = 'Missing some arguments.'

    return Response({
        'success': is_success,
        'error': not is_success,
        'message': message
    })


@api_view(['GET'])
@protected_resource()
def get_user_info(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'last_login': user.last_login,
        'date_joined': user.date_joined,
        'is_superuser': user.is_superuser
    })
