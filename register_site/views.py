import requests
from django.shortcuts import render, redirect
from scanner_engine.models import WatchersIndex
from scanner_engine.utils.utils import get_title, get_description, get_h1
from scanner_engine.utils.redirection.utils import run_redirection_scan
from scanner_engine.utils.watcher.utils import run_watcher_scan
from .forms import WatchersIndexForm, EntriesIndexForm, RedirectionsIndexForm
from .models import EntriesIndex
from .utils import parse_domain_name


def register_form(request):
    """
    Form used to register new Entry and Watcher in teh DB.
    It requires title, description and h1 for Watcher.
    """
    if not request.user.is_authenticated():
        return redirect("/accounts/login/")

    form_watcher = WatchersIndexForm(request.POST or None)
    form_site = EntriesIndexForm(request.POST or None)

    context = {
        'form_site': form_site,
        'form_addon': form_watcher,
        'message': 'Register new watcher'
    }

    if form_site.is_valid():
        new_entry = form_site.save(commit=False)
        new_entry.owner_username = request.user.username
        if not new_entry.alias:
            new_entry.alias = parse_domain_name(new_entry.url)
        new_entry.save()

    if form_watcher.is_valid():
        new_watcher = form_watcher.save(commit=False)
        new_watcher.entry = new_entry
        new_watcher.save()
        new_entry.watcher_exists = 1
        new_entry.save()

        """
        Scan newly added entry, to have a least one scan in the DB.
        It is necessary to display templates correctly.
        """
        run_watcher_scan(new_watcher)
        context = {
            'form_site': EntriesIndexForm,
            'form_addon': WatchersIndexForm,
            'message': 'Watcher registered correctly!'
        }
    return render(request, 'register_site/register_site.html', context)


def site_from_snapshot_form(request):
    """
    Form used to register new Entry and Watcher in teh DB.
    Title, description and h1 for Watcher are taken directly from the given site.
    """
    if not request.user.is_authenticated():
        return redirect("/accounts/login/")

    form_site = EntriesIndexForm(request.POST or None)

    context = {
        'form_site': form_site,
        'message': 'Register new watcher from snapshot'
    }

    if form_site.is_valid():
        new_entry = form_site.save(commit=False)
        new_entry.owner_username = request.user.username
        if not new_entry.alias:
            new_entry.alias = parse_domain_name(new_entry.url)

        # Get data necessary to register new site
        try:
            response = requests.get(new_entry.url, proxies={"http": "http://107.151.152.218:80"},
                                    headers={'user-agent': 'Scanner'})
        except requests.exceptions.RequestException as error:
            print ("Connection error : %s\n" % error)
            return render(request, 'register_site/error_page.html',
                          {'error_message': 'Error connecting with the given url.'})

        new_entry.save()
        new_watcher = WatchersIndex(
            title=get_title(response),
            description=get_description(response),
            h1=get_h1(response),
            entry=new_entry
        )
        new_watcher.save()
        new_entry.watcher_exists = 1
        new_entry.save()

        """
        Scan newly added entry, to have a least one scan in the DB.
        It is necessary to display templates correctly.
        """
        run_watcher_scan(new_watcher)
        context = {
            'form_site': EntriesIndexForm,
            'message': 'Watcher registered correctly!'
        }

    return render(request, "register_site/register_site.html", context)


def register_301_form(request):
    """
    Form used to register new Entry and Redirection in teh DB.
    """
    if not request.user.is_authenticated():
        return redirect("/accounts/login/")

    form_redirection = RedirectionsIndexForm(request.POST or None, initial={'status_code': 301})
    form_site = EntriesIndexForm(request.POST or None)

    context = {
        'form_site': form_site,
        'form_addon': form_redirection,
        'message': 'Register new redirection'
    }

    if form_site.is_valid():
        new_entry = form_site.save(commit=False)
        new_entry.owner_username = request.user.username
        if not new_entry.alias:
            new_entry.alias = parse_domain_name(new_entry.url)
        new_entry.save()

    if form_redirection.is_valid():
        new_redirection = form_redirection.save(commit=False)
        new_redirection.entry = new_entry
        new_redirection.status_code = 301
        new_redirection.base_url = new_entry.url
        new_redirection.save()
        new_entry.redirections_exists = 1
        new_entry.save()

        """
        Scan newly added entry, to have a least one scan in the DB.
        It is necessary to display templates correctly.
        """
        run_redirection_scan(new_redirection)
        context = {
            'form_site': EntriesIndexForm,
            'form_addon': RedirectionsIndexForm(initial={'status_code': 301}),
            'message': 'Redirection registered correctly!'
        }
    return render(request, 'register_site/register_site.html', context)


def delete_entry(request, entry_id=None):
    """
    Delete Entry with given id and all associated add-ons.
    """
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')

    if entry_id and len(EntriesIndex.objects.filter(id=entry_id)) > 0:
        entry = EntriesIndex.objects.get(id=entry_id)
        entry.delete()

    return redirect('/')
