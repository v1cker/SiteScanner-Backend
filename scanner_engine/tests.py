from django.test import TestCase
from register_site.models import EntriesIndex, WatchersIndex, RedirectionsIndex
from scanner_engine.models import ScannerLogs, WatcherScanResult, RedirectionScanResult
from .utils.watcher.utils import has_problems_watcher
from .utils.redirection.utils import has_problems_rediretion
from .tasks import automatic_scan_task


def create_test_models():
    entry = EntriesIndex(
        alias='test entry',
        owner_username='test',
        url='http://test.com/',
        watcher_exists=1,
        redirections_exists=1
    )
    entry.save()
    watcher = WatchersIndex(
        entry=entry,
        title='Test Title',
        description='Test Description',
        h1='Test h1'
    )
    watcher.save()
    redirection = RedirectionsIndex(
        entry=entry,
        base_url='http://base.com/',
        target_url='http://target.com/',
        status_code=301
    )
    redirection.save()


class AutomaticScanTaskTests(TestCase):

    def setUp(self):
        create_test_models()

    def test_automatic_scan(self):
        """
        Scan all entries in the database
        """
        # False prevents mail from being send
        automatic_scan_task(False)
        scanner_logs = ScannerLogs.objects.all()
        # One watcher and one redirection should be scanned
        self.assertEqual(len(scanner_logs), 2)


class UtilsOfScannerEngineTests(TestCase):

    def setUp(self):
        create_test_models()

    def test_has_problems_with_scan_without_problems(self):
        """
        If given scan don't have any problems
        return False
        """
        watcher = WatchersIndex.objects.get(id=1)
        watcher_scan = WatcherScanResult(
            watcher=watcher,
            status_code=200,
            title=watcher.title,
            description=watcher.description,
            h1=watcher.h1
        )
        response = has_problems_watcher(watcher_scan)
        self.assertEqual(response, False)
        redirection = RedirectionsIndex.objects.get(id=1)
        redirection_scan = RedirectionScanResult(
            redirection=redirection,
            base_url=redirection.base_url,
            target_url=redirection.target_url,
            status_code=redirection.status_code
        )
        response = has_problems_rediretion(redirection_scan)
        self.assertEqual(response, False)

    def test_has_problems_with_scan_with_problems(self):
        """
        If given scan have problems
        return True
        """
        watcher = WatchersIndex.objects.get(id=1)
        watcher_scan = WatcherScanResult(
            watcher=watcher,
            status_code=200,
            title='That is not valid',
            description=watcher.description,
            h1=watcher.h1
        )
        response = has_problems_watcher(watcher_scan)
        self.assertEqual(response, True)
        redirection = RedirectionsIndex.objects.get(id=1)
        redirection_scan = RedirectionScanResult(
            redirection=redirection,
            base_url=redirection.base_url,
            target_url=redirection.target_url,
            status_code=redirection.status_code+12
        )
        response = has_problems_rediretion(redirection_scan)
        self.assertEqual(response, True)

    def test_has_problems_watcher_with_wrong_type_of_argument(self):
        """
        If given argument is not an instance of desired ScanResult object
        throw a ValueError
        """
        self.assertRaises(ValueError, has_problems_watcher, 'This argument is not a scan object')
        self.assertRaises(ValueError, has_problems_rediretion, 'This is not valid either')
