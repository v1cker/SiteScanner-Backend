from django.shortcuts import render, redirect

from register_site.models import EntriesIndex, WatchersIndex, RedirectionsIndex
from scanner_engine.utils.redirection.utils import run_redirection_scan
from scanner_engine.utils.watcher.utils import run_watcher_scan
from .models import WatcherScanResult, RedirectionScanResult

# Create your views here.


def home(request):
    if not request.user.is_authenticated():
        return redirect("/accounts/login/")

    entries = EntriesIndex.objects.all()
    list_of_watcher_scans = []
    list_of_redirection_scans = []
    for entry in entries:
        # Show only entries that belong to current user
        if entry.owner_username == request.user.username:
            if entry.has_watcher():
                if len(WatchersIndex.objects.filter(entry=entry)) == 1:
                    watcher = WatchersIndex.objects.get(entry=entry)
                    watcher_scan_result = WatcherScanResult.objects.filter(watcher=watcher).order_by('-timestamp')[0]
                    list_of_watcher_scans.append(watcher_scan_result)
                else:
                    print ('Ivalid number of watchers')
                    entry.watcher_exists = 0
                    entry.save()
            if entry.has_redirections():
                if len(RedirectionsIndex.objects.filter(entry=entry)) > 0:
                    redirections = RedirectionsIndex.objects.filter(entry=entry)
                    for redirection in redirections:
                        redirection_scan_result = RedirectionScanResult.objects.filter(redirection=redirection).order_by('-timestamp')[0]
                        list_of_redirection_scans.append(redirection_scan_result)
                else:
                    print ('Ivalid number of redirections')
                    entry.redirections_exists = 0
                    entry.save()

    context = {
        "watchers": list_of_watcher_scans,
        "redirections": list_of_redirection_scans
    }
    return render(request, "home_view.html", context)


def update_scans(request, entry_id=None):
    if not request.user.is_authenticated():
        return redirect("/accounts/login/")

    if entry_id:
        entries_to_check = EntriesIndex.objects.filter(id=entry_id)
    else:
        entries_to_check = EntriesIndex.objects.all()

    for entry in entries_to_check:
        if entry.has_watcher():
            print ('watcher exists')
            if len(WatchersIndex.objects.filter(entry=entry)) == 1:
                run_watcher_scan(WatchersIndex.objects.get(entry=entry))
            else:
                print ('Invalid number of watchers for entry')
        if entry.has_redirections():
            print ('redirection exists')
            if len(RedirectionsIndex.objects.filter(entry=entry)) != 0:
                for redirection in RedirectionsIndex.objects.filter(entry=entry):
                    run_redirection_scan(redirection)
            else:
                entry.redirections_exists = 0
                entry.save()

    if 'next_url' in request.GET:
        return redirect("/" + request.GET['next_url'])
    else:
        return redirect("/")
