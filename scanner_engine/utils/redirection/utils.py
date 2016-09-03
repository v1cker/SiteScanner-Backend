import requests
import random
from scanner_engine.models import RedirectionScanResult, ScannerLogs
from scanner_engine.utils.utils import get_redirection_code


def run_redirection_scan(redirection, number_of_proxies_to_use=100):
    proxies_list = [
        'http://142.105.57.46:8888',
        'http://79.17.239.210:80',
        'http://142.105.57.46:8888',
        'http://97.85.189.196:80',
        'http://177.12.186.54:8080',
        'http://79.17.239.210:80'
    ]
    random.shuffle(proxies_list)
    if not number_of_proxies_to_use or number_of_proxies_to_use > len(proxies_list)-1:
        number_of_proxies_to_use = len(proxies_list)-1
    else:
        number_of_proxies_to_use -= 1
    headers = {'user-agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'}
    scan_result = RedirectionScanResult()
    proxy_index = 0
    proxies = {"http": proxies_list[proxy_index]}
    while True:
        try:
            response = requests.get(
                redirection.entry.url,
                proxies=proxies,
                headers=headers,
                timeout=10)
            break
        except requests.exceptions.Timeout as timeout_error:
            if proxy_index < number_of_proxies_to_use:
                proxy_index += 1
                proxies = {"http": proxies_list[proxy_index]}
                continue
            elif proxies:
                proxies = None
                continue
            scan_result.redirection = redirection
            scan_result.base_url = redirection.entry.url
            scan_result.target_url = 'Timeout'
            scan_result.status_code = 504
            scan_result.save()
            print(timeout_error.message)
            return False
        except requests.exceptions.RequestException as error:
            if proxy_index < number_of_proxies_to_use:
                proxy_index += 1
                proxies = {"http": proxies_list[proxy_index]}
                continue
            elif proxies:
                proxies = None
                continue
            print("Connection error : %s\n" % error)
            scan_result.redirection = redirection
            scan_result.base_url = redirection.entry.url
            scan_result.target_url = 'Error'
            scan_result.status_code = 418
            scan_result.save()
            return False

    scan_result.redirection = redirection
    scan_result.base_url = redirection.entry.url
    scan_result.target_url = response.url
    scan_result.status_code = get_redirection_code(response)
    scan_result.save()
    redirection.scan = scan_result
    redirection.save()
    if proxies:
        proxy = proxies['http']
    else:
        proxy = None
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
