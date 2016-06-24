from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import calculate_time_passed
from register_site.models import EntriesIndex, WatchersIndex
from scanner_engine.models import WatcherScanResult


def modify_site(request, entry_id=None):
    """
    Modify watcher of the entry with given id.
    Request needs to have attribute-value pair inside POST.
    """
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')

    # Check if given entry_id is present in the database
    if entry_id and len(EntriesIndex.objects.filter(id=entry_id)) > 0:

        # Check if attribute-value pair was given in the request
        if not 'attribute' in request.POST or not 'value' in request.POST:
            messages.add_message(request, messages.WARNING, "Data format error!")
            if 'next_url' in request.POST:
                return redirect("/"+request.POST['next_url'])
            else:
                return redirect("/")

        attribute_name = request.POST['attribute']
        new_value = request.POST['value']

        entry = EntriesIndex.objects.get(id=entry_id)
        if entry.has_watcher():
            if len(WatchersIndex.objects.filter(entry=entry)) != 1:
                raise ValueError('Wrong number of Watchers. Should be 1, found %d' % (
                    len(WatchersIndex.objects.filter(entry=entry))))

            watcher = WatchersIndex.objects.get(entry=entry)
            setattr(watcher, attribute_name, new_value)
            watcher.save()
            messages.add_message(request, messages.SUCCESS, "Attribute changed successfully!")

            if 'next_url' in request.POST:
                return redirect("/"+request.POST['next_url'])
            else:
                return redirect("/page_details/"+entry_id+"/")

    else:
        return render(request, 'register_site/error_page.html',
                      {'error_message': 'Site with given ID was not found in the database!'})


def page_details(request, entry_id=None):
    """
    Display site and its watcher to the user.
    """
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')

    if entry_id and len(EntriesIndex.objects.filter(id=entry_id)) > 0:

        entry = EntriesIndex.objects.get(id=entry_id)
        if entry.has_watcher():
            if len(WatchersIndex.objects.filter(entry=entry)) != 1:
                raise ValueError('Wrong number of Watchers. Should be 1, found %d' % (
                len(WatchersIndex.objects.filter(entry=entry))))
            watcher = WatchersIndex.objects.get(entry=entry)
            scan = WatcherScanResult.objects.filter(watcher=watcher).order_by('-timestamp')[0]
            time_since_last_scan = calculate_time_passed(scan.timestamp)
            context = {
                'scan': scan,
                'time_elapsed': time_since_last_scan
            }
            return render(request, 'manage_sites/site_details.html', context)

    else:
        return render(request, 'register_site/error_page.html',
                      {'error_message': 'Site with given ID was not found in the database!'})
