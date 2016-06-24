from django.shortcuts import render, redirect
from .models import SitesBackupIndex
from register_site.models import EntriesIndex
import requests
import os
import datetime


"""
Request conent of site with the given id
and save it to teh disk.
"""
def download_site(request, entry_id=None):
    if not request.user.is_authenticated():
        return redirect("/accounts/login/")

    if not entry_id or len(EntriesIndex.objects.filter(id=entry_id)) != 1:
        return render(request, 'register_site/error_page.html',
                      {'error_message': 'Site with given ID was not found in the database!'})

    entry = EntriesIndex.objects.get(id=entry_id)
    headers = {'user-agent': 'Scanner'}
    proxies = {"http": "http://107.151.152.218:80"}
    try:
        scan_result = requests.get(entry.url, proxies=proxies, headers=headers)
    except requests.exceptions.RequestException as error:
        print ("Connection error : %s\n" % error)
        return render(request, 'register_site/error_page.html',
                  {'error_message': 'There was an error connecting to the server at %s' % entry.url})

    if hasattr(scan_result, 'content'):

        # Delete elements that should not be in the folder name
        site_url = entry.url
        parts_to_delete = ['http://', 'https://', '.pl/', '.pl', '.eu/', '.eu', '.com/', '.com', '.info/', '.info']
        for phrase in parts_to_delete:
            site_url = site_url.replace(phrase, '')

        current_time = str(datetime.datetime.now())
        if not os.path.exists("sites_backup/backup_files/%s" % site_url):
            os.makedirs("sites_backup/backup_files/%s" % site_url)
        os.makedirs(os.path.join("sites_backup", "backup_files", site_url, site_url + "-" + current_time))

        with open(os.path.join("sites_backup", "backup_files", site_url,
                               site_url + "-" + current_time,
                               "index.html"), "w+") as f:
            f.write(scan_result.content)

    else:
        return render(request, 'register_site/error_page.html',
                      {'error_message': 'Invalid response object'})

    model_instance = SitesBackupIndex(
        entry=entry,
        path="%s/%s" % (site_url, site_url+str(datetime.datetime.now())),
        author=request.user.username
    )
    model_instance.save()

    if 'next_url' in request.GET:
        return redirect("/"+request.GET['next_url'])
    else:
        return redirect("/")
