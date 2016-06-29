from scanner_engine.models import ArchiveLocalCopy, ScannerLogs
import datetime
import os
import requests, shutil
from bs4 import BeautifulSoup


def download_all_images(response, resource_path='/resources/'):
    soup = BeautifulSoup(response.content)
    img_tags = soup.find_all('img')
    image_urls = []
    for img in img_tags:
        if response.url not in img['src']:
            image_urls.append(response.url + img['src'])
        else:
            image_urls.append(img['src'])
        # image_name = img['src'].split('/')[-1]
        # img['src'] = resource_path + image_name

    if not os.path.exists(resource_path):
        os.makedirs(resource_path)

    for url in set(image_urls):
        image_name = url.split('/')[-1]
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join(resource_path, image_name), 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)


def change_resource_path(soup, new_resource_path='resources/'):
    img_tags = soup.find_all('img')
    for img in img_tags:
        image_name = img['src'].split('/')[-1]
        img['src'] = new_resource_path + image_name
    return soup


def run_archive_copy(archive, proxy=None):
    proxies_list = {
        "France": "http://37.187.60.61",
        "Italy": "http://151.22.146.164:8080"
    }
    headers = {'user-agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0'}
    timeout_in_seconds = 60
    if not proxy:
        proxies = {"http": proxies_list["Italy"]}
    else:
        proxies = {"http": proxy}

    local_copy = ArchiveLocalCopy()
    try:
        response = requests.get(archive.url, proxies=proxies, headers=headers, timeout=timeout_in_seconds)
    except requests.exceptions.Timeout as timeout_error:
        log = ScannerLogs(proxy=str(proxy), addon=archive,
                          message='Time out error: ' + str(timeout_error.message))
        log.save()
        print (timeout_error.message)
        return False
    except requests.exceptions.RequestException as error:
        log = ScannerLogs(proxy=str(proxy), addon=archive,
                          message='Error: ' + str(error))
        log.save()
        print ("Connection error : %s\n" % error)
        return False

    if hasattr(response, 'content'):
        # Delete elements that should not be in the folder name
        site_url = archive.url
        parts_to_delete = ['http://', 'https://', '.pl/', '.pl', '.eu/', '.eu', '.com/', '.com', '.info/', '.info']
        for phrase in parts_to_delete:
            site_url = site_url.replace(phrase, '')

        current_time = str(datetime.datetime.now())
        backup_path = os.path.join("scanner_engine", "backup_files", site_url, site_url + "-" + current_time)

        if not os.path.exists("scanner_engine/backup_files/%s" % site_url):
            os.makedirs("scanner_engine/backup_files/%s" % site_url)
        os.makedirs(backup_path)

        download_all_images(response, os.path.join(backup_path, 'resources'))

        # Change file paths inside index.html
        soup = BeautifulSoup(response.content)
        soup = change_resource_path(soup)

        with open(os.path.join(backup_path, 'index.html'), 'w+') as f:
            f.write(str(soup))
    else:
        log = ScannerLogs(proxy=proxy, addon=archive,
                          message='Error: Invalid response object.')
        log.save()
        return False

    local_copy.archive = archive
    local_copy.url = archive.url
    local_copy.status_code = response.status_code
    local_copy.save()
    log = ScannerLogs(proxy=proxy, addon=local_copy.archive,
                      message='Success')
    log.save()
    return local_copy

