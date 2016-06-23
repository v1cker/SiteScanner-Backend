import requests

from scanner_engine.models import WatcherScanResult, ScannerLogs
from scanner_engine.utils.utils import get_title, get_description, get_h1


def run_watcher_scan(watcher, proxy=None):
    proxies_list = {
        "US": "http://107.151.152.218:80",
        "France": "http://37.187.60.61",
        "Italy": "http://151.22.146.164:8080"
    }
    headers = {'user-agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'}
    if not proxy:
        proxies = {"http": proxies_list["US"]}
    else:
        proxies = {"http": proxy}

    scan_result = WatcherScanResult()
    try:
        response = requests.get(watcher.entry.url, proxies=proxies, headers=headers)
    except requests.exceptions.RequestException as error:
        print ("Connection error : %s\n" % error)
        return False
    scan_result.watcher = watcher
    scan_result.status_code = response.status_code
    scan_result.title = get_title(response)
    scan_result.description = get_description(response)
    scan_result.h1 = get_h1(response)
    scan_result.save()
    watcher.last_scan_id = scan_result.id
    watcher.save()
    log = ScannerLogs(proxy=proxy, addon=scan_result.watcher)
    log.save()
    return scan_result


# Return True if error found
def has_problems_watcher(watcher_scan_result):
    if not isinstance(watcher_scan_result, WatcherScanResult):
        message = 'Given argument is not an instance of WatcherScanResult! %s' % (type(watcher_scan_result))
        raise ValueError(message)

    if watcher_scan_result.status_code != 200:
        return True
    if watcher_scan_result.title != watcher_scan_result.watcher.title:
        return True
    if watcher_scan_result.description != watcher_scan_result.watcher.description:
        return True
    if watcher_scan_result.h1 != watcher_scan_result.watcher.h1:
        return True
    return False
