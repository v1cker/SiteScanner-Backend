import requests

from scanner_engine.models import RedirectionScanResult, ScannerLogs
from scanner_engine.utils.utils import get_redirection_code


def run_redirection_scan(redirection, proxy=None):
    proxies_list = {
        "US": "http://107.151.152.218:80",
        "France": "http://37.187.60.61",
        "Italy": "http://151.22.146.164:8080"
    }
    headers = {'user-agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'}
    timeout_in_seconds = 20
    if not proxy:
        proxies = {"http": proxies_list["US"]}
    else:
        proxies = {"http": proxy}

    scan_result = RedirectionScanResult()
    try:
        response = requests.get(redirection.entry.url, proxies=proxies, headers=headers, timeout=timeout_in_seconds)
    except requests.exceptions.Timeout as timeout_error:
        scan_result.redirection = redirection
        scan_result.base_url = redirection.entry.url
        scan_result.target_url = redirection.entry.url
        scan_result.status_code = 504
        scan_result.save()
        print (timeout_error.message)
        return False
    except requests.exceptions.RequestException as error:
        print ("Connection error : %s\n" % error)
        return False

    scan_result.redirection = redirection
    scan_result.base_url = redirection.entry.url
    scan_result.target_url = response.url
    scan_result.status_code = get_redirection_code(response)
    scan_result.save()
    log = ScannerLogs(proxy=proxy, addon=scan_result.redirection)
    log.save()
    return scan_result


def has_problems_rediretion(redirection_scan_result):
    if not isinstance(redirection_scan_result, RedirectionScanResult):
        message = 'Given argument is not an instance of RedirectionScanResult! %s' % (type(redirection_scan_result))
        raise ValueError(message)

    if redirection_scan_result.target_url != redirection_scan_result.redirection.target_url:
        return True
    if redirection_scan_result.status_code != redirection_scan_result.redirection.status_code:
        return True
    return False
